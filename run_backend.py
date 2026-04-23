import uvicorn

from backend.main import app


if __name__ == "__main__":
    # Avoid uvicorn CLI reloader/worker spawning in restricted environments.
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

