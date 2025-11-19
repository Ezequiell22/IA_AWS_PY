import json
import time

from app.aws import get_sqs_client
from app import config
from app.queue import ensure_queue
from .engine import summarize


def process_message(body: dict) -> None:
    task = body.get("task")
    text = body.get("text", "")
    job_id = body.get("job_id")
    if task == "summarize":
        result = summarize(text)
        print(json.dumps({"job_id": job_id, "result": result}))


def run():
    url, _ = ensure_queue()
    client = get_sqs_client()
    while True:
        resp = client.receive_message(QueueUrl=url, MaxNumberOfMessages=5, WaitTimeSeconds=5)
        for msg in resp.get("Messages", []):
            try:
                body = json.loads(msg["Body"])  # type: ignore
                process_message(body)
            finally:
                client.delete_message(QueueUrl=url, ReceiptHandle=msg["ReceiptHandle"])  # type: ignore
        time.sleep(1)


if __name__ == "__main__":
    run()