import threading
from queue import Queue
from typing import Any, Dict

import boto3
from . import config


_fake_lock = threading.Lock()
_fake_queue: Queue[str] | None = None
_fake_url = "http://fake/sqs/ai-jobs"


class FakeSQSClient:
    def create_queue(self, QueueName: str) -> Dict[str, Any]:
        global _fake_queue
        with _fake_lock:
            if _fake_queue is None:
                _fake_queue = Queue()
        return {"QueueUrl": _fake_url}

    def get_queue_url(self, QueueName: str) -> Dict[str, Any]:
        return {"QueueUrl": _fake_url}

    def get_queue_attributes(self, QueueUrl: str, AttributeNames: list[str]) -> Dict[str, Any]:
        return {"Attributes": {"QueueArn": "arn:aws:sqs:fake:000000000000:ai-jobs"}}

    def send_message(self, QueueUrl: str, MessageBody: str) -> Dict[str, Any]:
        assert _fake_queue is not None
        _fake_queue.put(MessageBody)
        return {"MessageId": "fake-message-id"}

    def receive_message(self, QueueUrl: str, MaxNumberOfMessages: int, WaitTimeSeconds: int) -> Dict[str, Any]:
        msgs = []
        assert _fake_queue is not None
        for _ in range(MaxNumberOfMessages):
            if _fake_queue.empty():
                break
            body = _fake_queue.get()
            msgs.append({"Body": body, "ReceiptHandle": "fake-receipt"})
        return {"Messages": msgs}

    def delete_message(self, QueueUrl: str, ReceiptHandle: str) -> None:
        return None


def get_sqs_client():
    if config.AWS_FAKE == "1":
        return FakeSQSClient()
    return boto3.client(
        "sqs",
        region_name=config.AWS_REGION,
        endpoint_url=config.AWS_ENDPOINT,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    )