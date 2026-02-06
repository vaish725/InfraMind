"""
Data models for InfraMind.
Defines the structure for all incident-related data.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class LogLevel(str, Enum):
    """Log severity levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"


class LogEntry(BaseModel):
    """Represents a single log entry."""
    timestamp: datetime
    level: LogLevel
    service: str
    message: str
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    raw: str = ""  # Original raw log line


class MetricDataPoint(BaseModel):
    """Represents a single metric data point."""
    timestamp: datetime
    metric_name: str
    value: float
    unit: Optional[str] = None
    tags: Dict[str, str] = Field(default_factory=dict)


class MetricSummary(BaseModel):
    """Summary statistics for a metric."""
    metric_name: str
    start_time: datetime
    end_time: datetime
    min_value: float
    max_value: float
    avg_value: float
    current_value: float
    anomaly_detected: bool = False
    change_percent: Optional[float] = None


class TraceSpan(BaseModel):
    """Represents a single distributed trace span."""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    service: str
    operation: str
    start_time: datetime
    end_time: datetime
    duration_ms: float
    status: str  # OK, ERROR, TIMEOUT
    tags: Dict[str, str] = Field(default_factory=dict)
    error: Optional[str] = None


class ConfigChange(BaseModel):
    """Represents a configuration change."""
    timestamp: datetime
    file_path: str
    key: str
    old_value: Optional[str] = None
    new_value: str
    change_type: str = "modified"  # added, modified, deleted


class DeploymentEvent(BaseModel):
    """Represents a deployment event."""
    timestamp: datetime
    service: str
    version: str
    deployed_by: Optional[str] = None
    environment: str = "production"
    status: str = "success"  # success, failed, rolled_back


class UnifiedContext(BaseModel):
    """
    Unified context combining all data sources for Gemini analysis.
    This is what gets sent to the AI for reasoning.
    """
    incident_id: str
    time_range_start: datetime
    time_range_end: datetime
    
    # All data sources
    logs: List[LogEntry] = Field(default_factory=list)
    metrics: List[MetricSummary] = Field(default_factory=list)
    metric_data_points: List[MetricDataPoint] = Field(default_factory=list)
    traces: List[TraceSpan] = Field(default_factory=list)
    config_changes: List[ConfigChange] = Field(default_factory=list)
    deployment_events: List[DeploymentEvent] = Field(default_factory=list)
    
    # Metadata
    services_involved: List[str] = Field(default_factory=list)
    error_count: int = 0
    
    def to_context_string(self) -> str:
        """Convert to a formatted string for Gemini."""
        context_parts = []
        
        context_parts.append(f"## INCIDENT TIMELINE")
        context_parts.append(f"Time Range: {self.time_range_start} to {self.time_range_end}")
        context_parts.append(f"Services Involved: {', '.join(self.services_involved)}")
        context_parts.append(f"Total Errors: {self.error_count}\n")
        
        if self.deployment_events:
            context_parts.append("## DEPLOYMENT EVENTS")
            for event in sorted(self.deployment_events, key=lambda x: x.timestamp):
                context_parts.append(
                    f"[{event.timestamp}] {event.service} deployed version {event.version} "
                    f"(status: {event.status})"
                )
            context_parts.append("")
        
        if self.config_changes:
            context_parts.append("## CONFIGURATION CHANGES")
            for change in sorted(self.config_changes, key=lambda x: x.timestamp):
                context_parts.append(
                    f"[{change.timestamp}] {change.file_path}: {change.key} = "
                    f"{change.old_value} → {change.new_value}"
                )
            context_parts.append("")
        
        if self.metrics:
            context_parts.append("## METRICS SUMMARY")
            for metric in self.metrics:
                anomaly = " ⚠️ ANOMALY" if metric.anomaly_detected else ""
                change = f" ({metric.change_percent:+.1f}%)" if metric.change_percent else ""
                context_parts.append(
                    f"{metric.metric_name}: {metric.current_value} "
                    f"(min: {metric.min_value}, max: {metric.max_value}, "
                    f"avg: {metric.avg_value}){change}{anomaly}"
                )
            context_parts.append("")
        
        if self.logs:
            context_parts.append("## ERROR LOGS")
            error_logs = [log for log in self.logs if log.level in [LogLevel.ERROR, LogLevel.CRITICAL, LogLevel.FATAL]]
            for log in sorted(error_logs, key=lambda x: x.timestamp)[:50]:  # Limit to 50 errors
                context_parts.append(f"[{log.timestamp}] [{log.level}] {log.service}: {log.message}")
            context_parts.append("")
        
        if self.traces:
            context_parts.append("## TRACE ANALYSIS")
            error_traces = [t for t in self.traces if t.status != "OK"]
            for trace in sorted(error_traces, key=lambda x: x.start_time)[:20]:  # Limit to 20 traces
                context_parts.append(
                    f"[{trace.start_time}] {trace.service}.{trace.operation} "
                    f"({trace.duration_ms}ms) - {trace.status}"
                )
                if trace.error:
                    context_parts.append(f"  Error: {trace.error}")
            context_parts.append("")
        
        return "\n".join(context_parts)
