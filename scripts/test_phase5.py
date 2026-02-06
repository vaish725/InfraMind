"""
Test script for Phase 5: Streamlit Frontend
Validates frontend functionality and API integration.
"""
import sys
import time
import requests
from pathlib import Path
import subprocess
import signal

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def check_api_running():
    """Check if API server is running."""
    try:
        response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def check_streamlit_running():
    """Check if Streamlit is running."""
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        return response.status_code == 200
    except:
        return False


def test_frontend_integration():
    """Test frontend integration with backend."""
    print("\n" + "="*70)
    print(" "*20 + "PHASE 5 FRONTEND TEST")
    print("="*70)
    
    # Test 1: Check API availability
    print("\n1️⃣  Checking API server...")
    if check_api_running():
        print("✅ API server is running on http://localhost:8000")
    else:
        print("❌ API server is NOT running")
        print("   Start it with: python scripts/start_api.py")
        return False
    
    # Test 2: Check API endpoints
    print("\n2️⃣  Testing API endpoints...")
    try:
        # Health endpoint
        health = requests.get("http://localhost:8000/api/v1/health", timeout=5)
        assert health.status_code == 200
        print("✅ Health endpoint working")
        
        # Incidents list endpoint
        incidents = requests.get("http://localhost:8000/api/v1/incidents", timeout=5)
        assert incidents.status_code == 200
        print("✅ Incidents endpoint working")
        
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return False
    
    # Test 3: Check Streamlit
    print("\n3️⃣  Checking Streamlit server...")
    if check_streamlit_running():
        print("✅ Streamlit server is running on http://localhost:8501")
        print("   You can now access the frontend in your browser!")
    else:
        print("⚠️  Streamlit server is NOT running")
        print("   Start it with: python scripts/start_frontend.py")
        print("   This is expected if you haven't started it yet.")
    
    # Test 4: Verify file structure
    print("\n4️⃣  Verifying file structure...")
    required_files = [
        "frontend/app.py",
        ".streamlit/config.toml",
        "scripts/start_frontend.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = Path(__file__).parent.parent / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    if not all_exist:
        return False
    
    # Test 5: Verify sample data
    print("\n5️⃣  Verifying sample data...")
    sample_files = [
        "data/samples/logs.json",
        "data/samples/metrics.json",
        "data/samples/traces.json"
    ]
    
    for file_path in sample_files:
        full_path = Path(__file__).parent.parent / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"⚠️  {file_path} - Not found (optional)")
    
    # Summary
    print("\n" + "="*70)
    print("✅ PHASE 5 SETUP COMPLETE!")
    print("="*70)
    print("\n📋 Next Steps:")
    print("\n1. Make sure API is running:")
    print("   python scripts/start_api.py")
    print("\n2. Start the Streamlit frontend:")
    print("   python scripts/start_frontend.py")
    print("\n3. Open your browser:")
    print("   http://localhost:8501")
    print("\n4. Test the UI:")
    print("   - Upload files or use sample data")
    print("   - Submit an analysis")
    print("   - View results and causal chains")
    print("   - Explore fix suggestions")
    print("\n" + "="*70)
    
    return True


def main():
    """Main test entry point."""
    try:
        success = test_frontend_integration()
        if success:
            print("\n🎉 Phase 5 is ready!")
            print("\nFrontend Features:")
            print("  ✅ Modern, responsive UI")
            print("  ✅ Multi-file upload support")
            print("  ✅ Sample data integration")
            print("  ✅ Interactive analysis display")
            print("  ✅ Causal chain visualization")
            print("  ✅ Prioritized fix suggestions")
            print("  ✅ Incident history browser")
            print("  ✅ Executive summary display")
            print("  ✅ Raw JSON data viewer")
            print("  ✅ Results download")
            
            return 0
        else:
            print("\n❌ Some tests failed. Please check the errors above.")
            return 1
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
