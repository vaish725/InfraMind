"""
Comprehensive startup script for InfraMind.
Starts both API backend and Streamlit frontend.
"""
import sys
import time
import subprocess
import signal
import requests
from pathlib import Path

project_root = Path(__file__).parent.parent


def check_port_available(port):
    """Check if a port is available."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0


def wait_for_service(url, max_attempts=30):
    """Wait for a service to become available."""
    for i in range(max_attempts):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
    return False


def main():
    """Start both API and frontend."""
    print("=" * 70)
    print(" " * 20 + "🚀 STARTING INFRAMIND")
    print("=" * 70)
    
    processes = []
    
    try:
        # Start API server
        print("\n1️⃣  Starting FastAPI backend...")
        if not check_port_available(8000):
            print("⚠️  Port 8000 is already in use. API may already be running.")
        else:
            api_process = subprocess.Popen(
                [sys.executable, str(project_root / "scripts" / "start_api.py")],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            processes.append(("API", api_process))
            print("   Waiting for API to start...")
            
            if wait_for_service("http://localhost:8000/api/v1/health"):
                print("✅ API server started successfully")
                print("   URL: http://localhost:8000")
                print("   Docs: http://localhost:8000/docs")
            else:
                print("❌ Failed to start API server")
                return
        
        # Start Streamlit frontend
        print("\n2️⃣  Starting Streamlit frontend...")
        if not check_port_available(8501):
            print("⚠️  Port 8501 is already in use. Frontend may already be running.")
        else:
            streamlit_process = subprocess.Popen(
                [
                    "streamlit", "run",
                    str(project_root / "frontend" / "app.py"),
                    "--server.port=8501",
                    "--server.address=localhost"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            processes.append(("Streamlit", streamlit_process))
            print("   Waiting for Streamlit to start...")
            
            if wait_for_service("http://localhost:8501"):
                print("✅ Streamlit frontend started successfully")
                print("   URL: http://localhost:8501")
            else:
                print("❌ Failed to start Streamlit frontend")
                return
        
        # Success message
        print("\n" + "=" * 70)
        print("✅ INFRAMIND IS READY!")
        print("=" * 70)
        print("\n🌐 Access the application:")
        print("   Frontend: http://localhost:8501")
        print("   API:      http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
        print("\n💡 Press Ctrl+C to stop all services")
        print("=" * 70)
        
        # Keep running
        if processes:
            # Wait for user interrupt
            try:
                for name, process in processes:
                    process.wait()
            except KeyboardInterrupt:
                print("\n\n⚠️  Shutting down...")
        else:
            print("\n✅ Services already running. You're all set!")
            print("   Press Ctrl+C to exit this script.")
            print("   (Services will keep running in the background)")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    finally:
        # Cleanup
        if processes:
            print("\n🛑 Stopping services...")
            for name, process in processes:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"   Stopped {name}")
                except:
                    process.kill()
            print("✅ All services stopped")


if __name__ == "__main__":
    main()
