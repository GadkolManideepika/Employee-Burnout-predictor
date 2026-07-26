"""Small helper script to launch the backend and frontend together.

Usage: python start.py

It will:
  * verify that required packages are importable
  * start Flask backend in a subprocess
  * wait a couple of seconds for it to be ready and call /analyze once
  * launch the Streamlit dashboard in a second subprocess

Both subprocesses are left running; use Ctrl+C in this terminal to tear them down.

This is purely for local development convenience.  If you prefer to run the
components separately, the commands are the same as described in README.md.
"""
import os
import sys
import time

REQUIRED = ["flask", "streamlit", "transformers", "torch", "pandas", "requests"]


def check_deps():
    missing = []
    for pkg in REQUIRED:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print("The following dependencies are missing:", ", ".join(missing))
        print("Install them with: python -m pip install -r requirements.txt")
        sys.exit(1)


def start_process(cmd, **kwargs):
    print("Starting:", " ".join(cmd))
    return subprocess.Popen(cmd, **kwargs)


if __name__ == "__main__":
    import subprocess

    check_deps()

    cwd = os.getcwd()
    # 1. launch backend
    backend_proc = start_process([sys.executable, "backend/app.py"], cwd=cwd)

    # give the server a moment to boot
    time.sleep(3)
    try:
        import requests
        r = requests.get("http://127.0.0.1:5000/analyze")
        print("/analyze returned status", r.status_code, r.text)
    except Exception as e:
        print("WARNING: could not call backend analyze endpoint:", e)

    # 2. launch streamlit dashboard
    streamlit_proc = start_process(["streamlit", "run", "frontend/dashboard.py"], cwd=cwd)

    print("Both processes started. Press Ctrl+C in this terminal to stop.")

    # wait for either process to exit
    try:
        backend_proc.wait()
    except KeyboardInterrupt:
        pass
    try:
        streamlit_proc.terminate()
    except Exception:
        pass

    print("Shutting down.")
