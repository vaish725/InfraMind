"""
Custom exceptions for InfraMind application.
Provides specific error types for better error handling and debugging.
"""
from typing import Optional, Any, Dict


class InfraMindException(Exception):
    """Base exception for all InfraMind errors."""
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500
    ):
        self.message = message
        self.details = details or {}
        self.status_code = status_code
        super().__init__(self.message)


class ConfigurationError(InfraMindException):
    """Raised when there's a configuration issue."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=500)


class GeminiAPIError(InfraMindException):
    """Raised when Gemini API calls fail."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=502)


class ParsingError(InfraMindException):
    """Raised when data parsing fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=400)


class ValidationError(InfraMindException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=400)


class FileSizeError(InfraMindException):
    """Raised when uploaded file exceeds size limit."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=413)


class ContextLengthError(InfraMindException):
    """Raised when context exceeds maximum length."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=400)


class AnalysisError(InfraMindException):
    """Raised when analysis fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details, status_code=500)
