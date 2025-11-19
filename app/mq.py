import json
import threading
from queue import Queue
from typing import Any, Dict, Optional

import pika

from . import config


_lock = threading.Lock()
_fake_queue: Optional[Queue[str]] = None


class FakeMQ:
    def ensure_queue(self, name: str) -> None:
        global _fake_queue
        with _lock:
            if _fake_queue is None:
                _fake_queue = Queue()

    def publish(self, name: str, body: str) -> str:
        assert _fake_queue is not None
        _fake_queue.put(body)
        return "fake-message-id"

    def get_many(self, name: str, max_messages: int) -> list[Dict[str, Any]]:
        msgs = []
        assert _fake_queue is not None
        for _ in range(max_messages):
            if _fake_queue.empty():
                break
            body = _fake_queue.get()
            msgs.append({"body": body})
        return msgs


def get_channel():
    credentials = pika.PlainCredentials(config.MQ_USER, config.MQ_PASS)
    params = pika.ConnectionParameters(host=config.MQ_HOST, port=config.MQ_PORT, credentials=credentials)
    conn = pika.BlockingConnection(params)
    return conn.channel()


def ensure_queue():
    if config.MQ_FAKE == "1":
        mq = FakeMQ()
        mq.ensure_queue(config.MQ_QUEUE_NAME)
        return mq
    ch = get_channel()
    ch.queue_declare(queue=config.MQ_QUEUE_NAME, durable=False)
    return ch


def send_job(message: dict) -> str:
    body = json.dumps(message)
    if config.MQ_FAKE == "1":
        mq = ensure_queue()
        return mq.publish(config.MQ_QUEUE_NAME, body)  # type: ignore
    ch = ensure_queue()
    ch.basic_publish(exchange="", routing_key=config.MQ_QUEUE_NAME, body=body)  # type: ignore
    return "published"