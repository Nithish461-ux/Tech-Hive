#!/usr/bin/env python3
"""
Run both backend API and frontend web server
"""
import subprocess
import sys
import os
import time
from pathlib import Path

# Get project root
project_root = Path(__file__).parent
backend_dir = project_root / "Backend"
frontend_dir = project_root / "frontend"

# Change to project root to ensure imports work
os.chdir(project_root)

# Start backend server
print("\n[START] Starting backend server on http://localhost:8000")
print("=" * 60)

venv_python = backend_dir / "venv" / "Scripts" / "python.exe"
if venv_python.exists():
    backend_cmd = [str(venv_python), "-m", "uvicorn", "Backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
else:
    backend_cmd = ["python", "-m", "uvicorn", "Backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

env = os.environ.copy()
env["PYTHONPATH"] = str(project_root)
backend_process = subprocess.Popen(backend_cmd, cwd=str(project_root), env=env)

# Give backend time to start
time.sleep(2)

# Start frontend dev server
print("\n[START] Starting frontend server on http://localhost:3000")
print("=" * 60)

if not (frontend_dir / "node_modules").exists():
    print("[SETUP] Installing frontend dependencies...")
    install_result = subprocess.run(["npm", "install"], cwd=str(frontend_dir), check=False)
    if install_result.returncode != 0:
        raise SystemExit("Frontend dependency installation failed.")

frontend_cmd = ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000", "--strictPort"]
frontend_process = subprocess.Popen(frontend_cmd, cwd=str(frontend_dir), env=env)

print("\n[INFO] Both servers are running!")
print("Frontend: http://localhost:3000")
print("Backend:  http://localhost:8000")
print("API docs: http://localhost:8000/docs")
print("\nPress Ctrl+C to stop both servers")
print("=" * 60 + "\n")

try:
    backend_process.wait()
except KeyboardInterrupt:
    print("\n\nStopping servers...")
    backend_process.terminate()
    frontend_process.terminate()
    backend_process.wait()
    frontend_process.wait()
    sys.exit(0)
