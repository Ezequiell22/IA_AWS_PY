import os


MQ_HOST = os.getenv("MQ_HOST", "rabbitmq")
MQ_PORT = int(os.getenv("MQ_PORT", "5672"))
MQ_USER = os.getenv("MQ_USER", "user")
MQ_PASS = os.getenv("MQ_PASS", "pass")
MQ_QUEUE_NAME = os.getenv("MQ_QUEUE_NAME", "ai-jobs")
MQ_FAKE = os.getenv("MQ_FAKE", "0")