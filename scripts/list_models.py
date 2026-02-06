"""List available Gemini models."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google import genai
from backend.core.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

print("\n" + "="*60)
print("  Available Gemini Models")
print("="*60 + "\n")

try:
    models = client.models.list()
    for model in models:
        if hasattr(model, 'name') and hasattr(model, 'supported_generation_methods'):
            methods = model.supported_generation_methods if hasattr(model, 'supported_generation_methods') else []
            if 'generateContent' in methods or not methods:
                print(f"✓ {model.name}")
                if hasattr(model, 'description'):
                    print(f"  Description: {model.description}")
                print()
except Exception as e:
    print(f"Error listing models: {e}")
