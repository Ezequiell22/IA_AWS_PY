from fastapi import FastAPI
from fastapi import HTTPException

from .schemas import JobIn, JobOut, make_job_payload
from .queue import send_job


app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs", response_model=JobOut, status_code=202)
def create_job(payload: JobIn) -> JobOut:
    try:
        job = make_job_payload(payload)
        message_id = send_job(job)
        return JobOut(job_id=job["job_id"], message_id=message_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
