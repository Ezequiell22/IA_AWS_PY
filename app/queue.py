import json
from typing import Tuple

from .aws import get_sqs_client
from . import config


def ensure_queue() -> Tuple[str, str]:
    client = get_sqs_client()
    client.create_queue(QueueName=config.SQS_QUEUE_NAME)
    url = client.get_queue_url(QueueName=config.SQS_QUEUE_NAME)["QueueUrl"]
    attrs = client.get_queue_attributes(QueueUrl=url, AttributeNames=["QueueArn"])  # type: ignore
    return url, attrs["Attributes"]["QueueArn"]


def send_job(message: dict) -> str:
    url, _ = ensure_queue()
    body = json.dumps(message)
    client = get_sqs_client()
    resp = client.send_message(QueueUrl=url, MessageBody=body)
    return resp["MessageId"]