from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskType(str, Enum):
    summarize = "summarize"


class JobIn(BaseModel):
    text: str = Field(min_length=1)
    task: TaskType = TaskType.summarize


class JobOut(BaseModel):
    job_id: str
    message_id: str
    status: str = "queued"


def make_job_payload(data: JobIn) -> dict:
    job_id = str(uuid4())
    return {
        "job_id": job_id,
        "task": data.task,
        "text": data.text,
    }