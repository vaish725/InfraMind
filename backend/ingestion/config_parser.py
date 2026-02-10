"""
Configuration file parser for InfraMind.
Parses YAML, JSON, and ENV configuration files and detects changes.
"""
import yaml
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from dateutil import parser as date_parser
import logging

from backend.models import ConfigChange
from backend.core.exceptions import ParsingError

logger = logging.getLogger(__name__)


class ConfigParser:
    """Parse configuration files and detect changes."""
    
    def parse_file(self, file_content: str, file_format: str = "auto", file_path: str = "config") -> List[ConfigChange]:
        """
        Parse configuration file into ConfigChange objects.
        
        Args:
            file_content: Raw content of config file
            file_format: "yaml", "json", "env", or "auto" to detect
            file_path: Path/name of the config file
            
        Returns:
            List of ConfigChange objects
        """
        try:
            # Handle empty or whitespace-only content
            if not file_content or not file_content.strip():
                logger.warning(f"Empty config file provided: {file_path}")
                return []  # Return empty list for empty files instead of erroring
            
            if file_format == "auto":
                file_format = self._detect_format(file_content, file_path)
            
            if file_format == "yaml":
                config_dict = self._parse_yaml(file_content)
            elif file_format == "json":
                config_dict = self._parse_json(file_content)
            elif file_format == "env":
                config_dict = self._parse_env(file_content)
            else:
                raise ParsingError(f"Unsupported config format: {file_format}")
            
            # Handle None or empty dict results
            if not config_dict:
                logger.warning(f"Config file parsed to empty dictionary: {file_path}")
                return []
            
            # Convert to ConfigChange objects
            return self._dict_to_changes(config_dict, file_path)
            
        except ParsingError:
            # Re-raise ParsingError as-is
            raise
        except Exception as e:
            logger.error(f"Error parsing config file '{file_path}': {str(e)}")
            raise ParsingError(f"Failed to parse config file '{file_path}': {str(e)}")
    
    def _detect_format(self, content: str, file_path: str) -> str:
        """Detect config file format."""
        # Check file extension first
        if file_path.endswith(('.yaml', '.yml')):
            return "yaml"
        elif file_path.endswith('.json'):
            return "json"
        elif file_path.endswith(('.env', '.conf', '.cfg', '.ini', '.properties')):
            # .conf files (like postgresql.conf) are typically key=value format
            return "env"
        
        # Try to detect by content
        stripped_content = content.strip()
        
        if not stripped_content:
            return "env"  # Default for empty content
        
        # Check if it looks like JSON
        if stripped_content.startswith('{') or stripped_content.startswith('['):
            try:
                json.loads(content)
                return "json"
            except:
                pass
        
        # Try to parse as YAML (YAML is a superset of JSON, so check this after JSON)
        try:
            result = yaml.safe_load(content)
            # If it's a dict or list, it's probably YAML
            if isinstance(result, (dict, list)):
                return "yaml"
        except:
            pass
        
        # Default to ENV/conf format (most lenient)
        return "env"
    
    def _parse_yaml(self, content: str) -> Dict[str, Any]:
        """Parse YAML configuration."""
        try:
            # Strip whitespace
            content = content.strip()
            if not content:
                logger.warning("Empty YAML content provided")
                return {}
            
            result = yaml.safe_load(content)
            return result if result is not None else {}
        except yaml.YAMLError as e:
            error_msg = f"Invalid YAML: {str(e)}"
            raise ParsingError(error_msg)
    
    def _parse_json(self, content: str) -> Dict[str, Any]:
        """Parse JSON configuration."""
        try:
            # Strip whitespace
            content = content.strip()
            if not content:
                logger.warning("Empty JSON content provided")
                return {}
            
            result = json.loads(content)
            return result if result is not None else {}
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON at line {e.lineno}, column {e.colno}: {e.msg}"
            if e.pos < len(content):
                # Show a snippet around the error
                snippet_start = max(0, e.pos - 20)
                snippet_end = min(len(content), e.pos + 20)
                snippet = content[snippet_start:snippet_end]
                error_msg += f"\n  Near: ...{snippet}..."
            raise ParsingError(error_msg)
    
    def _parse_env(self, content: str) -> Dict[str, str]:
        """Parse ENV/conf file format (supports .env, .conf, postgresql.conf, etc.)."""
        config = {}
        lines = content.strip().split('\n')
        
        for line in lines:
            # Strip whitespace
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip comments (support both # and -- style comments)
            if line.startswith('#') or line.startswith('--') or line.startswith(';'):
                continue
            
            # Remove inline comments (both # and -- style)
            # But be careful with quoted values
            for comment_char in ['#', '--']:
                comment_pos = line.find(comment_char)
                if comment_pos > 0:
                    # Simple check: if not inside quotes, strip the comment
                    before_comment = line[:comment_pos]
                    if before_comment.count('"') % 2 == 0 and before_comment.count("'") % 2 == 0:
                        line = before_comment.strip()
                        break
            
            if not line:
                continue
            
            # Parse KEY=VALUE or KEY = VALUE format
            # Support both styles: KEY=VALUE and KEY = VALUE (with spaces)
            match = re.match(r'^([A-Za-z_][A-Za-z0-9_.-]*)\s*=\s*(.*)$', line)
            if match:
                key = match.group(1)
                value = match.group(2).strip()
                
                # Remove quotes if present
                if len(value) >= 2:
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                
                config[key] = value
        
        return config
    
    def _dict_to_changes(
        self, 
        config_dict: Dict[str, Any], 
        file_path: str,
        prefix: str = ""
    ) -> List[ConfigChange]:
        """Convert config dictionary to ConfigChange objects."""
        changes = []
        timestamp = datetime.now()
        
        for key, value in config_dict.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            # Recursively handle nested dictionaries
            if isinstance(value, dict):
                changes.extend(self._dict_to_changes(value, file_path, full_key))
            else:
                changes.append(ConfigChange(
                    timestamp=timestamp,
                    file_path=file_path,
                    key=full_key,
                    new_value=str(value),
                    change_type="current"  # Current state
                ))
        
        return changes
    
    def compare_configs(
        self,
        old_changes: List[ConfigChange],
        new_changes: List[ConfigChange]
    ) -> List[ConfigChange]:
        """
        Compare two sets of configurations and find differences.
        
        Args:
            old_changes: Previous configuration state
            new_changes: Current configuration state
            
        Returns:
            List of ConfigChange objects showing what changed
        """
        changes = []
        timestamp = datetime.now()
        
        # Create dictionaries for easy lookup
        old_dict = {c.key: c.new_value for c in old_changes}
        new_dict = {c.key: c.new_value for c in new_changes}
        
        # Find modified and added keys
        for key, new_value in new_dict.items():
            if key in old_dict:
                old_value = old_dict[key]
                if old_value != new_value:
                    changes.append(ConfigChange(
                        timestamp=timestamp,
                        file_path=new_changes[0].file_path if new_changes else "config",
                        key=key,
                        old_value=old_value,
                        new_value=new_value,
                        change_type="modified"
                    ))
            else:
                changes.append(ConfigChange(
                    timestamp=timestamp,
                    file_path=new_changes[0].file_path if new_changes else "config",
                    key=key,
                    new_value=new_value,
                    change_type="added"
                ))
        
        # Find deleted keys
        for key, old_value in old_dict.items():
            if key not in new_dict:
                changes.append(ConfigChange(
                    timestamp=timestamp,
                    file_path=old_changes[0].file_path if old_changes else "config",
                    key=key,
                    old_value=old_value,
                    new_value="",
                    change_type="deleted"
                ))
        
        return changes
    
    def filter_critical_changes(self, changes: List[ConfigChange]) -> List[ConfigChange]:
        """Filter to show only potentially critical configuration changes."""
        critical_keywords = [
            'timeout', 'connection', 'pool', 'max', 'limit', 'retry',
            'port', 'host', 'url', 'endpoint', 'database', 'db',
            'cache', 'memory', 'cpu', 'thread', 'worker'
        ]
        
        return [
            change for change in changes
            if any(keyword in change.key.lower() for keyword in critical_keywords)
        ]
