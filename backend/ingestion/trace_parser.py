"""
Trace parser for InfraMind.
Parses distributed trace spans and builds service dependency graphs.
"""
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Set
from dateutil import parser as date_parser
import logging

from backend.models import TraceSpan
from backend.core.exceptions import ParsingError

logger = logging.getLogger(__name__)


class TraceParser:
    """Parse distributed traces and analyze service dependencies."""
    
    def parse_file(self, file_content: str) -> List[TraceSpan]:
        """
        Parse trace file into TraceSpan objects.
        
        Args:
            file_content: Raw content of trace file (JSON format)
            
        Returns:
            List of TraceSpan objects
        """
        try:
            data = json.loads(file_content)
            
            if isinstance(data, list):
                return self._parse_span_list(data)
            elif isinstance(data, dict):
                # Support various structures
                spans = data.get('spans') or data.get('traces') or data.get('data')
                if isinstance(spans, list):
                    return self._parse_span_list(spans)
                else:
                    return self._parse_span_list([data])
            else:
                raise ParsingError("Unsupported trace format")
                
        except json.JSONDecodeError as e:
            raise ParsingError(f"Invalid JSON in trace file: {str(e)}")
        except Exception as e:
            logger.error(f"Error parsing traces: {str(e)}")
            raise ParsingError(f"Failed to parse traces: {str(e)}")
    
    def _parse_span_list(self, spans: List[Dict[str, Any]]) -> List[TraceSpan]:
        """Parse list of span dictionaries."""
        parsed_spans = []
        
        for span_data in spans:
            try:
                span = self._parse_single_span(span_data)
                if span:
                    parsed_spans.append(span)
            except Exception as e:
                logger.warning(f"Failed to parse span: {e}")
                continue
        
        return parsed_spans
    
    def _parse_single_span(self, span_data: Dict[str, Any]) -> Optional[TraceSpan]:
        """Parse a single span dictionary."""
        try:
            # Extract trace and span IDs
            trace_id = span_data.get('trace_id') or span_data.get('traceId') or span_data.get('trace')
            span_id = span_data.get('span_id') or span_data.get('spanId') or span_data.get('id')
            
            if not trace_id or not span_id:
                return None
            
            # Extract parent span ID
            parent_span_id = (
                span_data.get('parent_span_id') or 
                span_data.get('parentSpanId') or 
                span_data.get('parent_id')
            )
            
            # Extract service and operation
            service = (
                span_data.get('service') or 
                span_data.get('service_name') or 
                span_data.get('serviceName') or
                'unknown'
            )
            
            operation = (
                span_data.get('operation') or 
                span_data.get('operation_name') or 
                span_data.get('operationName') or
                span_data.get('name') or
                'unknown'
            )
            
            # Extract timestamps
            start_time_str = span_data.get('start_time') or span_data.get('startTime') or span_data.get('timestamp')
            end_time_str = span_data.get('end_time') or span_data.get('endTime')
            
            start_time = self._parse_timestamp(start_time_str)
            
            # Calculate duration
            duration_ms = span_data.get('duration') or span_data.get('duration_ms')
            
            if duration_ms:
                duration_ms = float(duration_ms)
                # Calculate end time if not provided
                if not end_time_str:
                    from datetime import timedelta
                    end_time = start_time + timedelta(milliseconds=duration_ms)
                else:
                    end_time = self._parse_timestamp(end_time_str)
            elif end_time_str:
                end_time = self._parse_timestamp(end_time_str)
                duration_ms = (end_time - start_time).total_seconds() * 1000
            else:
                # Default duration
                duration_ms = 0
                end_time = start_time
            
            # Extract status
            status = span_data.get('status') or span_data.get('status_code') or 'OK'
            status = status.upper()
            
            # Map status codes to meaningful names
            if status in ['200', '0', 'SUCCESS']:
                status = 'OK'
            elif status in ['500', '1', '2']:
                status = 'ERROR'
            elif 'TIMEOUT' in status or status == '504':
                status = 'TIMEOUT'
            
            # Extract tags
            tags = span_data.get('tags') or span_data.get('attributes') or {}
            if not isinstance(tags, dict):
                tags = {}
            
            # Extract error information
            error = span_data.get('error') or span_data.get('error_message')
            if not error and 'error' in tags:
                error = tags.get('error')
            
            return TraceSpan(
                trace_id=str(trace_id),
                span_id=str(span_id),
                parent_span_id=str(parent_span_id) if parent_span_id else None,
                service=service,
                operation=operation,
                start_time=start_time,
                end_time=end_time,
                duration_ms=duration_ms,
                status=status,
                tags=tags,
                error=error
            )
            
        except Exception as e:
            logger.warning(f"Failed to parse span: {e}")
            return None
    
    def _parse_timestamp(self, timestamp_str: Any) -> datetime:
        """Parse timestamp string or integer to datetime object."""
        if not timestamp_str:
            return datetime.now()
        
        try:
            # Handle Unix timestamps (in seconds or milliseconds)
            if isinstance(timestamp_str, (int, float)):
                # If it's a large number, it's likely in milliseconds
                if timestamp_str > 1e12:
                    return datetime.fromtimestamp(timestamp_str / 1000)
                else:
                    return datetime.fromtimestamp(timestamp_str)
            
            # Handle string timestamps
            return date_parser.parse(str(timestamp_str))
        except Exception as e:
            logger.warning(f"Failed to parse timestamp '{timestamp_str}': {e}")
            return datetime.now()
    
    def build_dependency_graph(self, spans: List[TraceSpan]) -> Dict[str, Set[str]]:
        """
        Build service dependency graph from spans.
        
        Returns:
            Dictionary mapping service names to set of services they depend on
        """
        dependencies = {}
        
        # Group spans by trace
        traces = {}
        for span in spans:
            if span.trace_id not in traces:
                traces[span.trace_id] = []
            traces[span.trace_id].append(span)
        
        # Analyze each trace
        for trace_id, trace_spans in traces.items():
            # Build span relationships
            span_map = {span.span_id: span for span in trace_spans}
            
            for span in trace_spans:
                if span.parent_span_id and span.parent_span_id in span_map:
                    parent_span = span_map[span.parent_span_id]
                    
                    # Parent service depends on current service
                    parent_service = parent_span.service
                    current_service = span.service
                    
                    if parent_service != current_service:
                        if parent_service not in dependencies:
                            dependencies[parent_service] = set()
                        dependencies[parent_service].add(current_service)
        
        return dependencies
    
    def find_error_chains(self, spans: List[TraceSpan]) -> List[List[TraceSpan]]:
        """
        Find chains of errors across spans (cascading failures).
        
        Returns:
            List of span chains that led to errors
        """
        error_chains = []
        
        # Group spans by trace
        traces = {}
        for span in spans:
            if span.trace_id not in traces:
                traces[span.trace_id] = []
            traces[span.trace_id].append(span)
        
        # Analyze each trace
        for trace_id, trace_spans in traces.items():
            # Find error spans
            error_spans = [s for s in trace_spans if s.status == 'ERROR']
            
            if error_spans:
                # Build span map for chain building
                span_map = {span.span_id: span for span in trace_spans}
                
                for error_span in error_spans:
                    # Trace back to root
                    chain = [error_span]
                    current = error_span
                    
                    while current.parent_span_id and current.parent_span_id in span_map:
                        parent = span_map[current.parent_span_id]
                        chain.insert(0, parent)  # Add to beginning
                        current = parent
                    
                    if len(chain) > 1:  # Only include if there's a chain
                        error_chains.append(chain)
        
        return error_chains
    
    def filter_by_service(self, spans: List[TraceSpan], services: List[str]) -> List[TraceSpan]:
        """Filter spans by service names."""
        return [span for span in spans if span.service in services]
    
    def filter_by_status(self, spans: List[TraceSpan], statuses: List[str]) -> List[TraceSpan]:
        """Filter spans by status."""
        return [span for span in spans if span.status in statuses]
    
    def get_slow_spans(self, spans: List[TraceSpan], threshold_ms: float = 1000) -> List[TraceSpan]:
        """Get spans that are slower than threshold."""
        return [span for span in spans if span.duration_ms > threshold_ms]
