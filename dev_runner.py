import os
import threading
import uvicorn

os.environ.setdefault("MQ_FAKE", "1")

from app.main import app
from worker.main import run as worker_run


def start_worker():
    t = threading.Thread(target=worker_run, daemon=True)
    t.start()
    return t


def main():
    start_worker()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()