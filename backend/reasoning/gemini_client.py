"""
Gemini API client wrapper for InfraMind.
Handles all interactions with Google's Gemini API.
"""
from google import genai
from google.genai import types
from typing import Optional, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

from backend.core.config import settings
from backend.core.exceptions import GeminiAPIError, ConfigurationError

logger = logging.getLogger(__name__)


class GeminiClient:
    """
    Wrapper for Google Gemini API.
    Provides retry logic, error handling, and response formatting.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Optional API key. Falls back to settings if not provided.
        """
        self.api_key = api_key or settings.gemini_api_key
        if not self.api_key:
            raise ConfigurationError(
                "Gemini API key not found. Please set GEMINI_API_KEY in .env file."
            )
        
        # Configure the client
        self.client = genai.Client(api_key=self.api_key)
        
        self.model_name = settings.gemini_model
        logger.info(f"Initialized Gemini client with model: {self.model_name}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def generate_content(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate content using Gemini API with retry logic.
        
        Args:
            prompt: The user prompt to send to Gemini
            system_instruction: Optional system instruction
            temperature: Sampling temperature (0.0 to 1.0)
            max_output_tokens: Maximum tokens in response
            
        Returns:
            Generated text response
            
        Raises:
            GeminiAPIError: If API call fails after retries
        """
        try:
            logger.info(f"Generating content with Gemini (temp={temperature})")
            
            # Prepare generation config
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                system_instruction=system_instruction if system_instruction else None
            )
            
            # Generate content
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            
            # Extract text from response
            if not response or not response.text:
                raise GeminiAPIError(
                    "Empty response from Gemini API",
                    details={"prompt_length": len(prompt)}
                )
            
            logger.info(f"Successfully generated {len(response.text)} characters")
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise GeminiAPIError(
                f"Failed to generate content: {str(e)}",
                details={
                    "model": self.model_name,
                    "prompt_length": len(prompt),
                    "error_type": type(e).__name__
                }
            )
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the Gemini API connection with a simple prompt.
        
        Returns:
            Dict with connection status and test response
        """
        try:
            test_prompt = "Respond with 'OK' if you can read this."
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=test_prompt
            )
            
            return {
                "status": "success",
                "model": self.model_name,
                "response": response.text,
                "message": "Gemini API connection successful"
            }
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return {
                "status": "error",
                "model": self.model_name,
                "error": str(e),
                "message": "Gemini API connection failed"
            }


# Singleton instance
_client_instance: Optional[GeminiClient] = None


def get_gemini_client() -> GeminiClient:
    """
    Get or create singleton Gemini client instance.
    
    Returns:
        GeminiClient instance
    """
    global _client_instance
    if _client_instance is None:
        _client_instance = GeminiClient()
    return _client_instance
