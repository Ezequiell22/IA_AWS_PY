import json
import time

from app import config
from app.mq import ensure_queue
from .engine import summarize


def process_message(body: dict) -> None:
    task = body.get("task")
    text = body.get("text", "")
    job_id = body.get("job_id")
    if task == "summarize":
        result = summarize(text)
        print(json.dumps({"job_id": job_id, "result": result}))


def run():
    ch_or_fake = ensure_queue()
    while True:
        if config.MQ_FAKE == "1":
            msgs = ch_or_fake.get_many(config.MQ_QUEUE_NAME, 5)  # type: ignore
            for m in msgs:
                body = json.loads(m["body"])  # type: ignore
                process_message(body)
        else:
            method_frame, header_frame, body = ch_or_fake.basic_get(queue=config.MQ_QUEUE_NAME, auto_ack=True)  # type: ignore
            if method_frame:
                process_message(json.loads(body))
        time.sleep(1)


if __name__ == "__main__":
    run()