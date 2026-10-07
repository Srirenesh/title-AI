#!/usr/bin/env python3
"""
Title-AI Unified Server Launcher.
Runs both the FastAPI AI Backend (Port 8000) and the Vite Frontend (Port 8443) concurrently.
"""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
VENV_PYTHON = BACKEND_DIR / ".venv" / ("Scripts" if sys.platform == "win32" else "bin") / "python"
VENV_UVICORN = BACKEND_DIR / ".venv" / ("Scripts" if sys.platform == "win32" else "bin") / "uvicorn"


def print_banner():
    print("\n" + "=" * 75)
    print("🚀 TITLE-AI UNIFIED APPLICATION LAUNCHER (Backend + Frontend + AI Model)")
    print("=" * 75)
    print("• 🌐 Frontend UI        : http://localhost:8443  (or preview panel)")
    print("• ⚡ FastAPI AI Backend : http://127.0.0.1:8000")
    print("• 📖 Interactive Docs   : http://127.0.0.1:8000/docs")
    print("• 🤖 Active AI Engine   : mradermacher/claude-3.7-sonnet-reasoning-gemma3-12B-GGUF")
    print("=" * 75)
    print("Press Ctrl+C at any time to stop all services.\n")


def start_services():
    print_banner()

    # Determine uvicorn executable
    if VENV_UVICORN.exists():
        backend_cmd = [str(VENV_UVICORN), "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    else:
        backend_cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

    # Frontend npm/vite command
    npm_bin = "npm.cmd" if sys.platform == "win32" else "npm"
    frontend_cmd = [npm_bin, "run", "dev"]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(BACKEND_DIR)

    print("[*] Starting FastAPI AI Backend on http://127.0.0.1:8000...")
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=str(BACKEND_DIR),
        env=env,
    )

    time.sleep(1)

    print("[*] Starting Vite React Frontend...")
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        cwd=str(ROOT_DIR),
        env=env,
    )

    def shutdown(sig=None, frame=None):
        print("\n\n[*] Gracefully shutting down Title-AI services...")
        try:
            frontend_proc.terminate()
            backend_proc.terminate()
        except Exception:
            pass
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        while True:
            time.sleep(1)
            # If any process unexpectedly died, report
            if backend_proc.poll() is not None:
                print(f"[!] Backend process exited with code {backend_proc.poll()}")
                break
            if frontend_proc.poll() is not None:
                print(f"[!] Frontend process exited with code {frontend_proc.poll()}")
                break
    except KeyboardInterrupt:
        shutdown()


if __name__ == "__main__":
    start_services()
