"""
Incident analysis endpoints.
"""
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
import logging
import json
from datetime import datetime

from backend.models.schemas import (
    AnalyzeIncidentRequest,
    AnalyzeIncidentResponse,
    IncidentStatus
)
from backend.models import DeploymentEvent
from backend.reasoning import ReasoningEngine
from backend.ingestion import DataUnifier
from backend.core.exceptions import GeminiAPIError, ParsingError, ValidationError

router = APIRouter()
logger = logging.getLogger(__name__)

# In-memory storage for demo (replace with database in production)
incidents_db = {}


@router.post(
    "/incidents/analyze",
    response_model=AnalyzeIncidentResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze incident",
    description="Submit incident data and get AI-powered root cause analysis"
)
async def analyze_incident(request: AnalyzeIncidentRequest):
    """
    Analyze an incident using Gemini AI.
    
    Accepts logs, metrics, traces, config changes, and deployments.
    Returns comprehensive root cause analysis with fix suggestions.
    """
    incident_id = request.incident_id
    logger.info(f"Analyzing incident {incident_id}")
    
    try:
        # Store incident in database
        incidents_db[incident_id] = {
            "status": IncidentStatus.ANALYZING,
            "created_at": datetime.now(),
            "request": request.model_dump()
        }
        
        # Parse and unify data
        logger.info("Parsing incident data...")
        unifier = DataUnifier()
        
        # Parse logs
        all_logs = []
        if request.log_files:
            for log_file in request.log_files:
                logs = unifier.log_parser.parse_file(
                    log_file.content,
                    source=log_file.source or "unknown"
                )
                all_logs.extend(logs)
        
        # Parse metrics
        all_metrics = []
        if request.metric_files:
            for metric_file in request.metric_files:
                metrics = unifier.metrics_parser.parse_file(metric_file.content)
                summaries = unifier.metrics_parser.create_summaries(metrics)
                all_metrics.extend(summaries)
        
        # Parse traces
        all_traces = []
        if request.trace_files:
            for trace_content in request.trace_files:
                # trace_files is List[str], not objects with .content
                traces = unifier.trace_parser.parse_file(trace_content)
                all_traces.extend(traces)
        
        # Parse configs
        config_changes = []
        if request.config_files:
            for config_file in request.config_files:
                changes = unifier.config_parser.parse_file(
                    config_file.content,
                    file_format=config_file.format or "auto",
                    file_path=config_file.path or "config"
                )
                config_changes.extend(changes)
            
            # If old and new configs provided, compare them
            if len(request.config_files) >= 2:
                old_configs = unifier.config_parser.parse_file(
                    request.config_files[0].content,
                    file_format=request.config_files[0].format or "auto",
                    file_path=request.config_files[0].path or "config"
                )
                new_configs = unifier.config_parser.parse_file(
                    request.config_files[1].content,
                    file_format=request.config_files[1].format or "auto",
                    file_path=request.config_files[1].path or "config"
                )
                config_changes = unifier.config_parser.compare_configs(old_configs, new_configs)
        
        # Create unified context
        logger.info("Creating unified context...")
        context = unifier.create_unified_context(
            logs=all_logs,
            metrics=all_metrics,
            traces=all_traces,
            configs=config_changes,
            deployments=request.deployments or [],
            time_window_minutes=request.time_window_minutes
        )
        
        # Override incident ID if provided
        context.incident_id = incident_id
        
        logger.info(f"Context created: {len(context.logs)} logs, {len(context.metrics)} metrics, {len(context.traces)} traces")
        
        # Perform RCA
        logger.info("Performing root cause analysis...")
        engine = ReasoningEngine()
        
        rca = await engine.analyze_incident(
            context=context,
            focus_area=request.focus_area,
            validate=True
        )
        
        # Generate summary if requested
        summary = None
        if request.include_summary:
            logger.info("Generating executive summary...")
            summary = await engine.generate_summary(rca)
        
        # Update incident status
        incidents_db[incident_id]["status"] = IncidentStatus.COMPLETED
        incidents_db[incident_id]["rca"] = rca.model_dump()
        incidents_db[incident_id]["completed_at"] = datetime.now()
        
        logger.info(f"Analysis completed for incident {incident_id}")
        
        return AnalyzeIncidentResponse(
            incident_id=incident_id,
            status=IncidentStatus.COMPLETED,
            rca=rca,
            summary=summary
        )
        
    except GeminiAPIError as e:
        logger.error(f"Gemini API error: {e}")
        incidents_db[incident_id]["status"] = IncidentStatus.FAILED
        incidents_db[incident_id]["error"] = str(e)
        
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Gemini API error: {str(e)}"
        )
    
    except (ParsingError, ValidationError) as e:
        logger.error(f"Data processing error: {e}")
        incidents_db[incident_id]["status"] = IncidentStatus.FAILED
        incidents_db[incident_id]["error"] = str(e)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Data processing error: {str(e)}"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        incidents_db[incident_id]["status"] = IncidentStatus.FAILED
        incidents_db[incident_id]["error"] = str(e)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/incidents/{incident_id}",
    response_model=AnalyzeIncidentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get incident analysis",
    description="Retrieve analysis results for a specific incident"
)
async def get_incident(incident_id: str):
    """
    Get incident analysis by ID.
    """
    if incident_id not in incidents_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident {incident_id} not found"
        )
    
    incident = incidents_db[incident_id]
    
    if incident["status"] == IncidentStatus.FAILED:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Incident analysis failed: {incident.get('error', 'Unknown error')}"
        )
    
    if incident["status"] == IncidentStatus.ANALYZING:
        return AnalyzeIncidentResponse(
            incident_id=incident_id,
            status=IncidentStatus.ANALYZING,
            rca=None,
            summary=None
        )
    
    # Convert stored RCA dict back to model
    from backend.models import RootCauseAnalysis
    rca = RootCauseAnalysis(**incident["rca"])
    
    return AnalyzeIncidentResponse(
        incident_id=incident_id,
        status=IncidentStatus.COMPLETED,
        rca=rca,
        summary=None
    )


@router.get(
    "/incidents",
    status_code=status.HTTP_200_OK,
    summary="List incidents",
    description="Get list of all analyzed incidents"
)
async def list_incidents(
    limit: int = 10,
    offset: int = 0,
    status_filter: Optional[IncidentStatus] = None
):
    """
    List all incidents with pagination.
    """
    incidents = list(incidents_db.items())
    
    # Filter by status if provided
    if status_filter:
        incidents = [
            (id, data) for id, data in incidents
            if data["status"] == status_filter
        ]
    
    # Pagination
    total = len(incidents)
    incidents = incidents[offset:offset + limit]
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "incidents": [
            {
                "incident_id": id,
                "status": data["status"],
                "created_at": data["created_at"],
                "completed_at": data.get("completed_at")
            }
            for id, data in incidents
        ]
    }


@router.post(
    "/incidents/analyze-files",
    response_model=AnalyzeIncidentResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze incident from file uploads",
    description="Upload log/metric/trace files and get analysis"
)
async def analyze_incident_from_files(
    incident_id: str = Form(...),
    log_files: List[UploadFile] = File(default=[]),
    metric_files: List[UploadFile] = File(default=[]),
    trace_files: List[UploadFile] = File(default=[]),
    config_files: List[UploadFile] = File(default=[]),
    deployments_json: Optional[str] = Form(default=None),
    time_window_minutes: Optional[int] = Form(default=None),
    focus_area: Optional[str] = Form(default=None),
    include_summary: bool = Form(default=True)
):
    """
    Analyze incident from uploaded files.
    
    This endpoint accepts file uploads instead of JSON.
    Useful for web UI integration.
    """
    logger.info(f"Analyzing incident {incident_id} from file uploads")
    
    try:
        # Read file contents
        log_data = []
        for log_file in log_files:
            content = await log_file.read()
            log_data.append({
                "content": content.decode('utf-8'),
                "source": log_file.filename
            })
        
        metric_data = []
        for metric_file in metric_files:
            content = await metric_file.read()
            metric_data.append({
                "content": content.decode('utf-8')
            })
        
        trace_data = []
        for trace_file in trace_files:
            content = await trace_file.read()
            trace_data.append(content.decode('utf-8'))
        
        config_data = []
        for config_file in config_files:
            content = await config_file.read()
            config_data.append({
                "content": content.decode('utf-8'),
                "path": config_file.filename,
                "format": "auto"
            })
        
        # Parse deployments if provided
        deployments = []
        if deployments_json:
            deployment_list = json.loads(deployments_json)
            for dep in deployment_list:
                deployments.append(DeploymentEvent(**dep))
        
        # Create request object
        from backend.models.schemas import LogFileData, MetricFileData, ConfigFileData
        
        request = AnalyzeIncidentRequest(
            incident_id=incident_id,
            log_files=[LogFileData(**log) for log in log_data],
            metric_files=[MetricFileData(**metric) for metric in metric_data],
            trace_files=trace_data,
            config_files=[ConfigFileData(**config) for config in config_data],
            deployments=deployments,
            time_window_minutes=time_window_minutes,
            focus_area=focus_area,
            include_summary=include_summary
        )
        
        # Call the main analysis endpoint
        return await analyze_incident(request)
        
    except Exception as e:
        logger.error(f"File upload error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File upload error: {str(e)}"
        )


@router.delete(
    "/incidents/{incident_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete incident",
    description="Delete an incident and its analysis"
)
async def delete_incident(incident_id: str):
    """
    Delete an incident.
    """
    if incident_id not in incidents_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident {incident_id} not found"
        )
    
    del incidents_db[incident_id]
    logger.info(f"Deleted incident {incident_id}")
    
    return None
