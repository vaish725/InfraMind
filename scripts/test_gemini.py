"""
Test script for Gemini API integration.
Validates API key and basic functionality.
"""
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.reasoning.gemini_client import GeminiClient
from backend.core.config import settings


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


async def test_gemini_connection():
    """Test basic Gemini API connection."""
    print_section("Testing Gemini API Connection")
    
    try:
        # Initialize client
        print("Initializing Gemini client...")
        client = GeminiClient()
        print(f"✓ Client initialized with model: {client.model_name}")
        
        # Test connection
        print("\nTesting API connection...")
        result = client.test_connection()
        
        if result["status"] == "success":
            print(f"✓ Connection successful!")
            print(f"  Model: {result['model']}")
            print(f"  Response: {result['response']}")
        else:
            print(f"✗ Connection failed!")
            print(f"  Error: {result['error']}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False
    
    return True


async def test_reasoning_capability():
    """Test Gemini's reasoning capability with a simple SRE scenario."""
    print_section("Testing Reasoning Capability")
    
    try:
        client = GeminiClient()
        
        # Create a simple debugging scenario
        prompt = """
You are an expert Site Reliability Engineer. Analyze this incident:

**Logs:**
2026-01-26 14:32:15 [ERROR] Service A: Connection timeout to database
2026-01-26 14:32:16 [ERROR] Service A: Failed to fetch user data
2026-01-26 14:32:20 [ERROR] Service B: Received 500 from Service A
2026-01-26 14:32:25 [ERROR] Service B: Request failed after 3 retries

**Metrics:**
- Service A error rate: 0% → 45% at 14:32
- Service A response time: 100ms → 5000ms at 14:32
- Database connections: 95/100 (max capacity)

**Question:** What is the root cause and what should we fix first?

Provide a brief analysis with:
1. Root cause
2. Why it happened
3. Immediate fix
"""
        
        print("Sending analysis request to Gemini...")
        response = await client.generate_content(
            prompt=prompt,
            temperature=0.3  # Lower temperature for more focused analysis
        )
        
        print("\n✓ Analysis completed!\n")
        print("="*60)
        print(response)
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"✗ Error during reasoning test: {str(e)}")
        return False


async def main():
    """Run all tests."""
    print_section("InfraMind - Gemini API Test Suite")
    print(f"Environment: {settings.app_env}")
    print(f"Model: {settings.gemini_model}")
    
    # Check if API key is set
    if not settings.gemini_api_key or settings.gemini_api_key == "your_gemini_api_key_here":
        print("\n✗ ERROR: GEMINI_API_KEY not set!")
        print("  Please:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your Gemini API key to .env")
        print("  3. Get a key from: https://ai.google.dev/")
        return
    
    # Run tests
    tests_passed = 0
    tests_total = 2
    
    if await test_gemini_connection():
        tests_passed += 1
    
    if await test_reasoning_capability():
        tests_passed += 1
    
    # Print summary
    print_section("Test Summary")
    print(f"Tests passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("\n✓ All tests passed! Gemini integration is working correctly.")
    else:
        print(f"\n✗ {tests_total - tests_passed} test(s) failed. Please check the errors above.")


if __name__ == "__main__":
    asyncio.run(main())
