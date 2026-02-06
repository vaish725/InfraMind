"""
API request/response schemas for InfraMind.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

from backend.models.rca import RootCauseAnalysis
from backend.models.incident import DeploymentEvent


class IncidentStatus(str, Enum):
    """Incident analysis status."""
    PENDING = "pending"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"


class LogFileData(BaseModel):
    """Log file data for analysis."""
    content: str = Field(..., description="Raw log file content")
    source: Optional[str] = Field(None, description="Source/service name")


class MetricFileData(BaseModel):
    """Metric file data for analysis."""
    content: str = Field(..., description="Raw metric file content (JSON)")


class ConfigFileData(BaseModel):
    """Configuration file data for analysis."""
    content: str = Field(..., description="Raw config file content")
    path: Optional[str] = Field(None, description="Config file path/name")
    format: Optional[str] = Field("auto", description="Config format: yaml, env, or auto")


class AnalyzeIncidentRequest(BaseModel):
    """Request to analyze an incident."""
    incident_id: str = Field(..., description="Unique incident identifier")
    log_files: Optional[List[LogFileData]] = Field(default=[], description="Log files to analyze")
    metric_files: Optional[List[MetricFileData]] = Field(default=[], description="Metric files to analyze")
    trace_files: Optional[List[str]] = Field(default=[], description="Trace files (JSON strings)")
    config_files: Optional[List[ConfigFileData]] = Field(default=[], description="Config files to analyze")
    deployments: Optional[List[DeploymentEvent]] = Field(default=[], description="Recent deployment events")
    time_window_minutes: Optional[int] = Field(None, description="Time window for filtering data (minutes)")
    focus_area: Optional[str] = Field(None, description="Focus area: configuration, performance, deployment, dependencies")
    include_summary: bool = Field(True, description="Include executive summary in response")


class AnalyzeIncidentResponse(BaseModel):
    """Response from incident analysis."""
    incident_id: str = Field(..., description="Incident identifier")
    status: IncidentStatus = Field(..., description="Analysis status")
    rca: Optional[RootCauseAnalysis] = Field(None, description="Root cause analysis results")
    summary: Optional[str] = Field(None, description="Executive summary")


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment name")
    gemini_model: str = Field(..., description="Gemini model in use")
    gemini_available: bool = Field(..., description="Whether Gemini API is available")
