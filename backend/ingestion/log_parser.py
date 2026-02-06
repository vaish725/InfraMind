"""
Log parser for InfraMind.
Supports JSON and plain text log formats.
"""
import json
import re
from datetime import datetime
from typing import List, Optional, Dict, Any
from dateutil import parser as date_parser
import logging

from backend.models import LogEntry, LogLevel
from backend.core.exceptions import ParsingError

logger = logging.getLogger(__name__)


class LogParser:
    """Parse logs from various formats into LogEntry objects."""
    
    # Common timestamp patterns
    TIMESTAMP_PATTERNS = [
        r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?',
        r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}',
        r'\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}',
    ]
    
    # Log level patterns
    LEVEL_PATTERN = r'\b(DEBUG|INFO|WARN(?:ING)?|ERROR|CRITICAL|FATAL)\b'
    
    def __init__(self):
        self.timestamp_regex = re.compile('|'.join(f'({p})' for p in self.TIMESTAMP_PATTERNS))
        self.level_regex = re.compile(self.LEVEL_PATTERN, re.IGNORECASE)
    
    def parse_file(self, file_content: str, source: str = "unknown", file_format: str = "auto") -> List[LogEntry]:
        """
        Parse log file content into LogEntry objects.
        
        Args:
            file_content: Raw content of the log file
            source: Source name for the logs (e.g., service name)
            file_format: "json", "text", or "auto" to detect
            
        Returns:
            List of parsed LogEntry objects
        """
        try:
            if file_format == "auto":
                file_format = self._detect_format(file_content)
            
            if file_format == "json":
                return self._parse_json_logs(file_content, source)
            else:
                return self._parse_text_logs(file_content, source)
        except Exception as e:
            logger.error(f"Error parsing log file: {str(e)}")
            raise ParsingError(
                message="Failed to parse log file",
                details={"format": file_format}
            )
    
    def _detect_format(self, content: str) -> str:
        """Detect if logs are JSON or plain text."""
        content = content.strip()
        if not content:
            return "text"
        
        # Try to parse first line as JSON
        first_line = content.split('\n')[0].strip()
        try:
            json.loads(first_line)
            return "json"
        except:
            return "text"
    
    def _parse_json_logs(self, content: str, source: str = "unknown") -> List[LogEntry]:
        """Parse JSON format logs (one JSON object per line)."""
        entries = []
        lines = content.strip().split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                log_obj = json.loads(line)
                entry = self._json_to_log_entry(log_obj, source)
                if entry:
                    entries.append(entry)
            except json.JSONDecodeError as e:
                logger.warning(f"Invalid JSON on line {line_num}: {e}")
                # Try to parse as text
                text_entry = self._parse_text_line(line, source)
                if text_entry:
                    entries.append(text_entry)
        
        return entries
    
    def _json_to_log_entry(self, log_obj: Dict[str, Any], source: str = "unknown") -> Optional[LogEntry]:
        """Convert JSON log object to LogEntry."""
        try:
            # Extract timestamp (try various field names)
            timestamp_str = (
                log_obj.get('timestamp') or 
                log_obj.get('time') or 
                log_obj.get('@timestamp') or
                log_obj.get('ts') or
                datetime.now().isoformat()
            )
            timestamp = self._parse_timestamp(timestamp_str)
            
            # Extract log level
            level_str = (
                log_obj.get('level') or 
                log_obj.get('severity') or 
                log_obj.get('log_level') or
                'INFO'
            ).upper()
            level = self._parse_log_level(level_str)
            
            # Extract service name
            service = (
                log_obj.get('service') or 
                log_obj.get('service_name') or
                log_obj.get('app') or
                log_obj.get('application') or
                source
            )
            
            # Extract message
            message = (
                log_obj.get('message') or 
                log_obj.get('msg') or
                log_obj.get('text') or
                str(log_obj)
            )
            
            # Extract trace/span IDs if present
            trace_id = log_obj.get('trace_id') or log_obj.get('traceId')
            span_id = log_obj.get('span_id') or log_obj.get('spanId')
            
            # Extract remaining fields as metadata
            metadata = {
                k: v for k, v in log_obj.items()
                if k not in {'timestamp', 'time', '@timestamp', 'ts', 'level', 
                            'severity', 'log_level', 'service', 'service_name', 
                            'app', 'application', 'message', 'msg', 'text',
                            'trace_id', 'traceId', 'span_id', 'spanId'}
            }
            
            return LogEntry(
                timestamp=timestamp,
                level=level,
                service=service,
                message=message,
                trace_id=trace_id,
                span_id=span_id,
                metadata=metadata,
                raw=json.dumps(log_obj)
            )
            
        except Exception as e:
            logger.warning(f"Failed to parse JSON log entry: {e}")
            return None
    
    def _parse_text_logs(self, content: str, source: str = "unknown") -> List[LogEntry]:
        """Parse plain text logs."""
        entries = []
        lines = content.strip().split('\n')
        
        current_entry = None
        
        for line in lines:
            line = line.rstrip()
            if not line:
                continue
            
            # Try to parse as a new log entry
            new_entry = self._parse_text_line(line, source)
            
            if new_entry:
                # Save previous entry if exists
                if current_entry:
                    entries.append(current_entry)
                current_entry = new_entry
            elif current_entry:
                # Continuation of previous entry (e.g., stack trace)
                current_entry.message += '\n' + line
                current_entry.raw += '\n' + line
        
        # Don't forget the last entry
        if current_entry:
            entries.append(current_entry)
        
        return entries
    
    def _parse_text_line(self, line: str, source: str = "unknown") -> Optional[LogEntry]:
        """Parse a single line of text log."""
        try:
            # Extract timestamp
            timestamp_match = self.timestamp_regex.search(line)
            if timestamp_match:
                timestamp_str = timestamp_match.group(0)
                timestamp = self._parse_timestamp(timestamp_str)
                remaining = line[timestamp_match.end():].strip()
            else:
                timestamp = datetime.now()
                remaining = line
            
            # Extract log level
            level_match = self.level_regex.search(remaining)
            if level_match:
                level_str = level_match.group(1).upper()
                level = self._parse_log_level(level_str)
                message = remaining[level_match.end():].strip()
            else:
                level = LogLevel.INFO
                message = remaining
            
            # Clean up message (remove common prefixes)
            message = re.sub(r'^\[.*?\]\s*', '', message)
            message = message.strip()
            
            if not message:
                return None
            
            return LogEntry(
                timestamp=timestamp,
                level=level,
                service=source,
                message=message,
                trace_id=None,
                span_id=None,
                metadata={},
                raw=line
            )
            
        except Exception as e:
            logger.warning(f"Failed to parse text log line: {e}")
            return None
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse timestamp string to datetime object."""
        if not timestamp_str:
            return datetime.now()
        
        try:
            # Handle Unix timestamps
            if timestamp_str.isdigit():
                timestamp = int(timestamp_str)
                # If it's a large number, it's likely in milliseconds
                if timestamp > 1e12:
                    return datetime.fromtimestamp(timestamp / 1000)
                else:
                    return datetime.fromtimestamp(timestamp)
            
            # Use dateutil parser for flexible parsing
            return date_parser.parse(timestamp_str)
        except Exception as e:
            logger.warning(f"Failed to parse timestamp '{timestamp_str}': {e}")
            return datetime.now()
    
    def _parse_log_level(self, level_str: str) -> LogLevel:
        """Parse log level string to LogLevel enum."""
        level_str = level_str.upper()
        
        # Map variations to standard levels
        level_map = {
            'DEBUG': LogLevel.DEBUG,
            'INFO': LogLevel.INFO,
            'WARN': LogLevel.WARNING,
            'WARNING': LogLevel.WARNING,
            'ERROR': LogLevel.ERROR,
            'ERR': LogLevel.ERROR,
            'CRITICAL': LogLevel.CRITICAL,
            'CRIT': LogLevel.CRITICAL,
            'FATAL': LogLevel.CRITICAL,
        }
        
        return level_map.get(level_str, LogLevel.INFO)
    
    def filter_by_level(self, entries: List[LogEntry], levels: List[str]) -> List[LogEntry]:
        """Filter log entries by level."""
        level_enums = [self._parse_log_level(level) for level in levels]
        return [entry for entry in entries if entry.level in level_enums]
    
    def filter_by_service(self, entries: List[LogEntry], services: List[str]) -> List[LogEntry]:
        """Filter log entries by service name."""
        return [entry for entry in entries if entry.service in services]
    
    def filter_by_time_range(
        self, 
        entries: List[LogEntry], 
        start_time: datetime, 
        end_time: datetime
    ) -> List[LogEntry]:
        """Filter log entries by time range."""
        return [
            entry for entry in entries 
            if start_time <= entry.timestamp <= end_time
        ]
