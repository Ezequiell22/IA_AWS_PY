import os


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localstack:4566")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
SQS_QUEUE_NAME = os.getenv("SQS_QUEUE_NAME", "ai-jobs")
AWS_FAKE = os.getenv("AWS_FAKE", "0")