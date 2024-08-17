import os

DATABASE_URL = os.getenv('DATABASE_URL', 'klickr.db')
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://redis:6379')

MINIO_BUCKET = os.getenv("MINIO_BUCKET", "klicker")
MINIO_BASE_URL = os.getenv("MINIO_BASE_URL", "minio:9000")

MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin123")

UPLOADS_FOLDER = os.getenv('UPLOADS_FOLDER', 'data/klickr')
