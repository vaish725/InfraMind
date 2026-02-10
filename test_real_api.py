#!/usr/bin/env python3
"""
Quick test to verify real Gemini API integration is working.
This script will make a simple request and check for demo mode indicators.
"""

import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Health check passed")
        print(f"   Gemini Model: {data.get('gemini_model')}")
        print(f"   Gemini Available: {data.get('gemini_available')}")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        return False

def test_real_analysis():
    """Test that analysis uses real Gemini, not demo mode."""
    print("\n🔍 Testing real Gemini analysis...")
    
    # Simple test data
    payload = {
        "incident_id": "test-real-api-verification",
        "log_files": [
            {
                "content": "2026-02-09 10:00:00 ERROR Database connection timeout after 30s",
                "source": "test-service"
            }
        ],
        "include_summary": True
    }
    
    print("📤 Sending test request...")
    response = requests.post(
        f"{API_URL}/api/v1/incidents/analyze",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        
        # Check for demo mode indicators
        summary = data.get('summary', '')
        is_demo = 'DEMO MODE' in summary or 'FALLBACK MODE' in summary
        
        if is_demo:
            print(f"⚠️  Analysis returned with demo/fallback mode")
            print(f"   This usually means API rate limit or configuration issue")
            print(f"   Summary: {summary}")
            return False
        else:
            print(f"✅ Real Gemini analysis confirmed!")
            print(f"   Incident ID: {data.get('incident_id')}")
            print(f"   Status: {data.get('status')}")
            if data.get('rca'):
                rca = data['rca']
                print(f"   Root Cause: {rca.get('root_cause', 'N/A')[:100]}...")
                print(f"   Confidence: {rca.get('overall_confidence')}")
            return True
    else:
        print(f"❌ Analysis request failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def main():
    print("=" * 60)
    print("🧪 InfraMind Real API Integration Test")
    print("=" * 60)
    
    # Test health
    if not test_health():
        print("\n❌ Health check failed. Is the backend running?")
        return
    
    # Test real analysis
    test_real_analysis()
    
    print("\n" + "=" * 60)
    print("📋 Test Complete")
    print("=" * 60)
    print("\n💡 Tips:")
    print("   - If you see 'FALLBACK MODE', check your API rate limits")
    print("   - If analysis fails, verify GEMINI_API_KEY in .env")
    print("   - Check backend logs for 'Sending to Gemini AI for reasoning...'")

if __name__ == "__main__":
    main()
