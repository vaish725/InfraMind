"""
Startup script for InfraMind Streamlit frontend.
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Run streamlit
if __name__ == "__main__":
    import subprocess
    
    frontend_path = project_root / "frontend" / "app.py"
    
    print("=" * 70)
    print("Starting InfraMind Streamlit Frontend")
    print("=" * 70)
    print(f"Frontend: {frontend_path}")
    print(f"URL: http://localhost:8501")
    print("=" * 70)
    
    subprocess.run([
        "streamlit",
        "run",
        str(frontend_path),
        "--server.port=8501",
        "--server.address=localhost"
    ])
