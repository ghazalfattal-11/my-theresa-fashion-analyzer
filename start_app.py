"""
This file is  to run both FastAPI backend and Streamlit frontend

"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit
        import fastapi
        import uvicorn
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\nPlease install dependencies:")
        print("pip install streamlit fastapi uvicorn")
        return False

def start_fastapi():
    """Start FastAPI backend"""
    print("\n🚀 Starting FastAPI backend...")
    
    # Use CREATE_NEW_CONSOLE on Windows to open in new window
    if sys.platform == "win32":
        return subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--reload"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        return subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--reload"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

def start_streamlit():
    """Start Streamlit frontend"""
    print("🎨 Starting Streamlit frontend...")
    
    # Use CREATE_NEW_CONSOLE on Windows to open in new window
    if sys.platform == "win32":
        return subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "frontend/app.py", 
             "--server.headless", "true"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        return subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "frontend/app.py",
             "--server.headless", "true"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

def main():
    print("="*70)
    print("Fashion Image Analysis - Startup Script")
    print("="*70)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if frontend exists
    if not Path("frontend/app.py").exists():
        print("❌ Frontend not found at frontend/app.py")
        sys.exit(1)
    
    print("\n📋 Starting services...")
    print("   - FastAPI backend: http://127.0.0.1:8000")
    print("   - Streamlit frontend: http://localhost:8501")
    print("\n⚠️  Two new console windows will open (don't close them!)")
    
    try:
        # Start FastAPI
        fastapi_process = start_fastapi()
        print("   ✅ FastAPI started in new window")
        time.sleep(3)  # Wait for FastAPI to start
        
        # Start Streamlit
        streamlit_process = start_streamlit()
        print("   ✅ Streamlit started in new window")
        time.sleep(5)  # Wait for Streamlit to start
        
        print("\n" + "="*70)
        print("✅ Both services started successfully!")
        print("="*70)
        print("\n🌐 Access the application:")
        print("   Frontend (Streamlit): http://localhost:8501")
        print("   Backend API (FastAPI): http://127.0.0.1:8000/docs")
        print("="*70)
        print("\n💡 Opening browser...")
        
        # Open browser
        time.sleep(2)
        webbrowser.open("http://localhost:8501")
        
        print("\n✅ Browser opened!")
        print("\n⚠️  To stop the services:")
        print("   - Close the two console windows that opened")
        print("   - Or press Ctrl+C in those windows")
        print("\nThis window can be closed now.")
        
        input("\nPress Enter to exit this window...")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping services...")
        try:
            fastapi_process.terminate()
            streamlit_process.terminate()
        except:
            pass
        print("✅ Services stopped")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTry running manually:")
        print("  Terminal 1: python -m uvicorn app.main:app --reload")
        print("  Terminal 2: python -m streamlit run frontend/app.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
