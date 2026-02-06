"""
Metrics parser for InfraMind.
Parses time-series metrics data and detects anomalies.
"""
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dateutil import parser as date_parser
import logging

from backend.models import MetricDataPoint, MetricSummary
from backend.core.exceptions import ParsingError

logger = logging.getLogger(__name__)


class MetricsParser:
    """Parse metrics from various formats and calculate summaries."""
    
    def __init__(self, anomaly_threshold: float = 2.0):
        """
        Initialize metrics parser.
        
        Args:
            anomaly_threshold: Standard deviations from mean to flag anomaly
        """
        self.anomaly_threshold = anomaly_threshold
    
    def parse_file(self, file_content: str) -> List[MetricDataPoint]:
        """
        Parse metrics file into MetricDataPoint objects.
        
        Args:
            file_content: Raw content of metrics file (JSON format)
            
        Returns:
            List of MetricDataPoint objects
        """
        try:
            data = json.loads(file_content)
            
            # Support various JSON structures
            if isinstance(data, list):
                return self._parse_list_format(data)
            elif isinstance(data, dict):
                return self._parse_dict_format(data)
            else:
                raise ParsingError("Unsupported metrics format")
                
        except json.JSONDecodeError as e:
            raise ParsingError(f"Invalid JSON in metrics file: {str(e)}")
        except Exception as e:
            logger.error(f"Error parsing metrics: {str(e)}")
            raise ParsingError(f"Failed to parse metrics: {str(e)}")
    
    def _parse_list_format(self, data: List[Dict[str, Any]]) -> List[MetricDataPoint]:
        """
        Parse metrics in list format:
        [
          {"timestamp": "...", "metric": "cpu", "value": 75.5, "tags": {...}},
          ...
        ]
        """
        metrics = []
        
        for item in data:
            try:
                timestamp_str = item.get('timestamp') or item.get('time') or datetime.now().isoformat()
                timestamp = self._parse_timestamp(timestamp_str)
                
                metric_name = item.get('metric') or item.get('name') or item.get('metric_name')
                if not metric_name:
                    continue
                
                value = float(item.get('value', 0))
                unit = item.get('unit')
                tags = item.get('tags', {})
                
                metrics.append(MetricDataPoint(
                    timestamp=timestamp,
                    metric_name=metric_name,
                    value=value,
                    unit=unit,
                    tags=tags
                ))
            except Exception as e:
                logger.warning(f"Failed to parse metric item: {e}")
                continue
        
        return metrics
    
    def _parse_dict_format(self, data: Dict[str, Any]) -> List[MetricDataPoint]:
        """
        Parse metrics in dict format:
        {
          "metrics": {
            "cpu": [{"timestamp": "...", "value": 75.5}, ...],
            "memory": [...]
          }
        }
        """
        metrics = []
        
        # Try to find metrics data
        metrics_data = data.get('metrics') or data.get('data') or data
        
        for metric_name, values in metrics_data.items():
            if not isinstance(values, list):
                # Single value
                try:
                    timestamp = self._parse_timestamp(data.get('timestamp', datetime.now().isoformat()))
                    value = float(values) if not isinstance(values, dict) else float(values.get('value', 0))
                    
                    metrics.append(MetricDataPoint(
                        timestamp=timestamp,
                        metric_name=metric_name,
                        value=value
                    ))
                except Exception as e:
                    logger.warning(f"Failed to parse metric {metric_name}: {e}")
                continue
            
            # Multiple values
            for item in values:
                try:
                    if isinstance(item, dict):
                        timestamp_str = item.get('timestamp') or item.get('time') or datetime.now().isoformat()
                        timestamp = self._parse_timestamp(timestamp_str)
                        value = float(item.get('value', 0))
                        unit = item.get('unit')
                        tags = item.get('tags', {})
                    else:
                        # Simple value
                        timestamp = datetime.now()
                        value = float(item)
                        unit = None
                        tags = {}
                    
                    metrics.append(MetricDataPoint(
                        timestamp=timestamp,
                        metric_name=metric_name,
                        value=value,
                        unit=unit,
                        tags=tags
                    ))
                except Exception as e:
                    logger.warning(f"Failed to parse metric value for {metric_name}: {e}")
                    continue
        
        return metrics
    
    def create_summaries(
        self, 
        data_points: List[MetricDataPoint],
        previous_baseline: Optional[Dict[str, float]] = None
    ) -> List[MetricSummary]:
        """
        Create metric summaries with anomaly detection.
        
        Args:
            data_points: List of metric data points
            previous_baseline: Optional baseline values for change detection
            
        Returns:
            List of MetricSummary objects
        """
        # Group by metric name
        grouped = {}
        for point in data_points:
            if point.metric_name not in grouped:
                grouped[point.metric_name] = []
            grouped[point.metric_name].append(point)
        
        summaries = []
        
        for metric_name, points in grouped.items():
            if not points:
                continue
            
            values = [p.value for p in points]
            current_value = points[-1].value if points else 0  # Most recent value
            
            # Get time range
            timestamps = [p.timestamp for p in points]
            start_time = min(timestamps)
            end_time = max(timestamps)
            
            # Calculate statistics
            min_val = min(values)
            max_val = max(values)
            avg_val = sum(values) / len(values)
            
            # Calculate standard deviation for anomaly detection
            variance = sum((x - avg_val) ** 2 for x in values) / len(values)
            std_dev = variance ** 0.5
            
            # Detect anomaly
            anomaly_detected = False
            if std_dev > 0:
                z_score = abs((current_value - avg_val) / std_dev)
                anomaly_detected = z_score > self.anomaly_threshold
            
            # Calculate change percentage if baseline provided
            change_percent = None
            if previous_baseline and metric_name in previous_baseline:
                baseline = previous_baseline[metric_name]
                if baseline > 0:
                    change_percent = ((current_value - baseline) / baseline) * 100
                    # Also flag as anomaly if change is drastic
                    if abs(change_percent) > 50:  # 50% change
                        anomaly_detected = True
            
            summaries.append(MetricSummary(
                metric_name=metric_name,
                start_time=start_time,
                end_time=end_time,
                min_value=min_val,
                max_value=max_val,
                avg_value=avg_val,
                current_value=current_value,
                anomaly_detected=anomaly_detected,
                change_percent=change_percent
            ))
        
        return summaries
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse timestamp string to datetime object."""
        try:
            return date_parser.parse(timestamp_str)
        except Exception as e:
            logger.warning(f"Failed to parse timestamp '{timestamp_str}': {e}")
            return datetime.now()
    
    def filter_by_time_range(
        self,
        data_points: List[MetricDataPoint],
        start: datetime,
        end: datetime
    ) -> List[MetricDataPoint]:
        """Filter metric data points by time range."""
        return [
            point for point in data_points
            if start <= point.timestamp <= end
        ]
    
    def get_metric_names(self, data_points: List[MetricDataPoint]) -> List[str]:
        """Get list of unique metric names."""
        return list(set(point.metric_name for point in data_points))
