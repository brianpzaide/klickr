from PIL import Image
import os
import logging
import pathlib
from . import config
from .utils import minio_client

from celery import Celery

logger = logging.getLogger('WORKER')
celery = Celery('tasks', broker=config.CELERY_BROKER_URL)

SIZE_MAP = {
    'small': (128, 128),
    'medium': (256, 256),
    'large': (512, 512)
}

def get_path(photo_id, ext):
    return os.path.join(config.UPLOADS_FOLDER, str(photo_id), f'original.{ext}')

@celery.task
def generate_thumbnail(photo_id, size, ext):
    print(os.getcwd())
    original_path = get_path(photo_id, ext)
    thumb_path = original_path.replace('original', size)
    ext = original_path.split(".")[-1]

    pathlib.Path(original_path).parent.mkdir(parents=True, exist_ok=True)

    generate_thumbnail_disk(photo_id, size, ext)
    
    minio_client.fput_object(file_path=thumb_path, bucket_name=config.MINIO_BUCKET, object_name=f"{photo_id}/{size}.{ext}")
    
    logging.info('Thumbnail of size {} saved to minio for photo {}'.format(size, photo_id))
    

def generate_thumbnail_disk(photo_id, size, ext):
    logging.info('Thumbnail of size {size} requested for photo {photo_id}')
    original_path = get_path(photo_id, ext)
    image = Image.open(original_path)
    image.thumbnail(SIZE_MAP[size])
    image.save(original_path.replace('original', size))
    logging.info(f'Thumbnail of size {size} generated for photo {photo_id}')