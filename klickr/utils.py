from typing import Tuple
import pathlib
import sqlite3
import json
from . import config

from minio import Minio

minio_client = Minio(
    config.MINIO_BASE_URL,
    access_key= config.MINIO_ACCESS_KEY,
    secret_key= config.MINIO_SECRET_KEY,
    secure=False,
)

if not minio_client.bucket_exists(config.MINIO_BUCKET):
    minio_client.make_bucket(config.MINIO_BUCKET)

policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetObject", "s3:PutObject"],
            "Resource": [f"arn:aws:s3:::{config.MINIO_BUCKET}/*"]
        }
    ]
}

minio_client.set_bucket_policy(config.MINIO_BUCKET, json.dumps(policy))

def setup_db():
    with sqlite3.connect(config.DATABASE_URL) as conn:
        cursor = conn.cursor()
        with open("schema.sql", 'r') as file:
            sql_statements = file.read()
        cursor.executescript(sql_statements)
        conn.commit()


def process_row(row: Tuple[str]):
    photo_id = row[0]
    data = {
        'id': photo_id
    }

    for size in ['original', 'small', 'medium', 'large']:
        data[size] = f'/photos/{photo_id}/{size}'

    return data


def save_file(file, photo_id, image_type, ext="jpg"):
    photo_folder = config.UPLOADS_FOLDER + f'/{photo_id}'
    photo_folder = pathlib.Path(photo_folder)

    photo_folder.mkdir(exist_ok=True, parents=True)

    photo_path = photo_folder.joinpath(f'{image_type}.{ext}')
    with photo_path.open('wb') as f:
        f.write(file.read())

    minio_client.fput_object(file_path=str(photo_path), bucket_name=config.MINIO_BUCKET, object_name=f"{photo_id}/{image_type}.{ext}")
