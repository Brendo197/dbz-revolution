import subprocess
import os
import threading

process = None


def read_stream(stream):
    for line in iter(stream.readline, ''):
        if line:
            print(line.rstrip(), flush=True)


def start_server():
    global process

    if process and process.poll() is None:
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(base_dir)

    venv_python = os.path.join(
        root_dir,
        ".venv",
        "Scripts",
        "python.exe"
    )

    process = subprocess.Popen(
        [
            venv_python,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8000"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    threading.Thread(target=read_stream, args=(process.stdout,), daemon=True).start()
    threading.Thread(target=read_stream, args=(process.stderr,), daemon=True).start()


def stop_server():
    global process
    if process:
        process.terminate()
        process = None
