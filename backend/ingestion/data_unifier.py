"""
Data unifier for InfraMind.
Combines data from all parsers into unified context for analysis.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from backend.models import (
    LogEntry, MetricSummary, TraceSpan, ConfigChange, 
    DeploymentEvent, UnifiedContext
)
from backend.ingestion.log_parser import LogParser
from backend.ingestion.metrics_parser import MetricsParser
from backend.ingestion.config_parser import ConfigParser
from backend.ingestion.trace_parser import TraceParser

logger = logging.getLogger(__name__)


class DataUnifier:
    """Unifies data from multiple sources into a single context."""
    
    def __init__(self):
        self.log_parser = LogParser()
        self.metrics_parser = MetricsParser()
        self.config_parser = ConfigParser()
        self.trace_parser = TraceParser()
    
    def _compare_timestamps(self, dt1: datetime, dt2: datetime) -> bool:
        """Compare two datetimes, handling timezone-aware and naive datetimes."""
        # Make both naive for comparison
        if dt1.tzinfo is not None:
            dt1 = dt1.replace(tzinfo=None)
        if dt2.tzinfo is not None:
            dt2 = dt2.replace(tzinfo=None)
        return dt1 >= dt2
    
    def create_unified_context(
        self,
        logs: List[LogEntry],
        metrics: List[MetricSummary],
        traces: List[TraceSpan],
        configs: List[ConfigChange],
        deployments: List[DeploymentEvent],
        time_window_minutes: Optional[int] = None
    ) -> UnifiedContext:
        """
        Create unified context from all data sources.
        
        Args:
            logs: Parsed log entries
            metrics: Parsed metric summaries
            traces: Parsed trace spans
            configs: Configuration changes
            deployments: Deployment events
            time_window_minutes: Optional time window to filter data (in minutes from now)
            
        Returns:
            UnifiedContext with all data combined
        """
        # Filter by time window if specified
        if time_window_minutes:
            from datetime import timezone
            cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=time_window_minutes)
            
            # Make cutoff_time naive if we have naive timestamps
            logs = [log for log in logs if self._compare_timestamps(log.timestamp, cutoff_time)]
            metrics = [metric for metric in metrics if self._compare_timestamps(metric.start_time, cutoff_time)]
            traces = [trace for trace in traces if self._compare_timestamps(trace.start_time, cutoff_time)]
            configs = [config for config in configs if self._compare_timestamps(config.timestamp, cutoff_time)]
            deployments = [dep for dep in deployments if self._compare_timestamps(dep.timestamp, cutoff_time)]
        
        # Sort everything by time for coherent narrative (normalize timezones first)
        logs.sort(key=lambda x: x.timestamp.replace(tzinfo=None) if x.timestamp.tzinfo else x.timestamp)
        metrics.sort(key=lambda x: x.start_time.replace(tzinfo=None) if x.start_time.tzinfo else x.start_time)
        traces.sort(key=lambda x: x.start_time.replace(tzinfo=None) if x.start_time.tzinfo else x.start_time)
        configs.sort(key=lambda x: x.timestamp.replace(tzinfo=None) if x.timestamp.tzinfo else x.timestamp)
        deployments.sort(key=lambda x: x.timestamp.replace(tzinfo=None) if x.timestamp.tzinfo else x.timestamp)
        
        # Calculate time range (normalize timezones)
        all_timestamps = []
        if logs:
            all_timestamps.extend([log.timestamp.replace(tzinfo=None) if log.timestamp.tzinfo else log.timestamp for log in logs])
        if metrics:
            all_timestamps.extend([m.start_time.replace(tzinfo=None) if m.start_time.tzinfo else m.start_time for m in metrics])
            all_timestamps.extend([m.end_time.replace(tzinfo=None) if m.end_time.tzinfo else m.end_time for m in metrics])
        if traces:
            all_timestamps.extend([t.start_time.replace(tzinfo=None) if t.start_time.tzinfo else t.start_time for t in traces])
            all_timestamps.extend([t.end_time.replace(tzinfo=None) if t.end_time.tzinfo else t.end_time for t in traces])
        
        if all_timestamps:
            time_range_start = min(all_timestamps)
            time_range_end = max(all_timestamps)
        else:
            time_range_start = datetime.now()
            time_range_end = datetime.now()
        
        # Generate incident ID
        import uuid
        incident_id = str(uuid.uuid4())
        
        # Identify services involved
        services = set()
        for log in logs:
            services.add(log.service)
        for trace in traces:
            services.add(trace.service)
        for deployment in deployments:
            services.add(deployment.service)
        
        # Count errors
        error_count = len([log for log in logs if log.level.value in ["ERROR", "CRITICAL"]])
        error_count += len([trace for trace in traces if trace.status in ["ERROR", "TIMEOUT"]])
        
        return UnifiedContext(
            incident_id=incident_id,
            time_range_start=time_range_start,
            time_range_end=time_range_end,
            logs=logs,
            metrics=metrics,
            traces=traces,
            config_changes=configs,
            deployment_events=deployments,
            services_involved=list(services),
            error_count=error_count
        )
    
    def from_files(
        self,
        log_files: Optional[List[Dict[str, str]]] = None,
        metric_files: Optional[List[Dict[str, str]]] = None,
        trace_files: Optional[List[str]] = None,
        config_files: Optional[List[Dict[str, Any]]] = None,
        deployment_data: Optional[List[DeploymentEvent]] = None,
        time_window_minutes: Optional[int] = None
    ) -> UnifiedContext:
        """
        Create unified context by parsing files.
        
        Args:
            log_files: List of dicts with 'content' and optional 'source'
            metric_files: List of dicts with 'content'
            trace_files: List of trace file contents
            config_files: List of dicts with 'content', 'format', and 'path'
            deployment_data: Pre-parsed deployment events
            time_window_minutes: Optional time window filter
            
        Returns:
            UnifiedContext with parsed data
        """
        logs = []
        metrics = []
        traces = []
        configs = []
        deployments = deployment_data or []
        
        # Parse logs
        if log_files:
            for log_file in log_files:
                try:
                    source = log_file.get('source', 'unknown')
                    parsed_logs = self.log_parser.parse_file(log_file['content'], source)
                    logs.extend(parsed_logs)
                    logger.info(f"Parsed {len(parsed_logs)} log entries from {source}")
                except Exception as e:
                    logger.error(f"Failed to parse log file: {e}")
        
        # Parse metrics
        if metric_files:
            for metric_file in metric_files:
                try:
                    parsed_metrics = self.metrics_parser.parse_file(metric_file['content'])
                    summaries = self.metrics_parser.create_summaries(parsed_metrics)
                    metrics.extend(summaries)
                    logger.info(f"Parsed {len(summaries)} metric summaries")
                except Exception as e:
                    logger.error(f"Failed to parse metric file: {e}")
        
        # Parse traces
        if trace_files:
            for trace_content in trace_files:
                try:
                    parsed_traces = self.trace_parser.parse_file(trace_content)
                    traces.extend(parsed_traces)
                    logger.info(f"Parsed {len(parsed_traces)} trace spans")
                except Exception as e:
                    logger.error(f"Failed to parse trace file: {e}")
        
        # Parse configs
        if config_files:
            for config_file in config_files:
                try:
                    file_format = config_file.get('format', 'auto')
                    file_path = config_file.get('path', 'config')
                    parsed_configs = self.config_parser.parse_file(
                        config_file['content'],
                        file_format,
                        file_path
                    )
                    configs.extend(parsed_configs)
                    logger.info(f"Parsed {len(parsed_configs)} config entries from {file_path}")
                except Exception as e:
                    logger.error(f"Failed to parse config file: {e}")
        
        return self.create_unified_context(
            logs=logs,
            metrics=metrics,
            traces=traces,
            configs=configs,
            deployments=deployments,
            time_window_minutes=time_window_minutes
        )
    
    def filter_by_severity(
        self,
        context: UnifiedContext,
        min_log_level: str = "WARNING",
        include_anomalies: bool = True,
        include_errors: bool = True
    ) -> UnifiedContext:
        """
        Filter context to focus on important events.
        
        Args:
            context: Original unified context
            min_log_level: Minimum log level to include
            include_anomalies: Include metrics with detected anomalies
            include_errors: Include error traces
            
        Returns:
            Filtered UnifiedContext
        """
        # Filter logs by level
        log_levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
        min_level = log_levels.get(min_log_level.upper(), 2)
        
        filtered_logs = [
            log for log in context.logs
            if log_levels.get(log.level.value, 0) >= min_level
        ]
        
        # Filter metrics to anomalies
        filtered_metrics = context.metrics
        if include_anomalies:
            filtered_metrics = [
                metric for metric in filtered_metrics
                if metric.anomaly_detected
            ]
        
        # Filter traces to errors
        filtered_traces = context.traces
        if include_errors:
            filtered_traces = [
                trace for trace in filtered_traces
                if trace.status == "ERROR"
            ]
        
        return UnifiedContext(
            incident_id=context.incident_id,
            time_range_start=context.time_range_start,
            time_range_end=context.time_range_end,
            logs=filtered_logs,
            metrics=filtered_metrics,
            traces=filtered_traces,
            config_changes=context.config_changes,  # Keep all config changes
            deployment_events=context.deployment_events,  # Keep all deployments
            services_involved=context.services_involved,
            error_count=len(filtered_logs) + len(filtered_traces)
        )
    
    def enrich_context(self, context: UnifiedContext) -> UnifiedContext:
        """
        Enrich context with additional analysis.
        
        - Build service dependency graph
        - Find error chains
        - Correlate events by time
        
        Args:
            context: Original unified context
            
        Returns:
            Enriched UnifiedContext with additional metadata
        """
        # Build dependency graph from traces
        if context.traces:
            dependency_graph = self.trace_parser.build_dependency_graph(context.traces)
            logger.info(f"Built dependency graph with {len(dependency_graph)} services")
            
            # Find error chains
            error_chains = self.trace_parser.find_error_chains(context.traces)
            logger.info(f"Found {len(error_chains)} error chains")
        
        # Find temporal correlations
        # (This is where we could add more sophisticated correlation logic)
        
        return context
    
    def get_summary_stats(self, context: UnifiedContext) -> Dict[str, Any]:
        """Get summary statistics about the unified context."""
        return {
            "incident_id": context.incident_id,
            "total_logs": len(context.logs),
            "error_logs": len([log for log in context.logs if log.level.value in ["ERROR", "CRITICAL"]]),
            "total_metrics": len(context.metrics),
            "anomalous_metrics": len([m for m in context.metrics if m.anomaly_detected]),
            "total_traces": len(context.traces),
            "error_traces": len([t for t in context.traces if t.status == "ERROR"]),
            "config_changes": len(context.config_changes),
            "deployments": len(context.deployment_events),
            "services_involved": context.services_involved,
            "time_range": {
                "start": context.time_range_start,
                "end": context.time_range_end
            }
        }
