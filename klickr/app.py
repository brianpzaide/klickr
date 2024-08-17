import logging
import sqlite3

from io import BytesIO

from flask import Flask, render_template, redirect, request, url_for, send_file, abort

from celery import Celery
from .tasks import generate_thumbnail

from . import config
from .utils import process_row, save_file, minio_client

logger = logging.Logger('WEBAPP')

app = Flask(__name__)

celery = Celery(__name__, broker=config.CELERY_BROKER_URL)

@app.route('/')
def index():
    with sqlite3.connect(config.DATABASE_URL) as conn:
        cursor = conn.cursor()
        rows = cursor.execute('SELECT * FROM photos ORDER BY id DESC LIMIT 50').fetchall()
        print(rows)

    photos = [process_row(row) for row in rows]
    return render_template('index.html', photos=photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        photo = request.files.get('photo')
        pfname = photo.filename
        if pfname == '':
            return render_template('upload.html', error="Please select a photo")

        fileformat = pfname.split(".")[-1]
        if fileformat not in ["jpg", "jpeg", "png"]:
            return render_template("upload.html", error="Invalid file format")

        with sqlite3.connect(config.DATABASE_URL) as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO photos(photo_name) VALUES(?)', (pfname,))
            conn.commit()
            photo_id = cur.lastrowid

        save_file(photo, photo_id, 'original', ext=fileformat)
        logging.info('Uploading photo with ID {}'.format(photo_id))
        for size in ['small', 'medium', 'large']:
            logging.info('Submitting task to worker queue. GENERATE_THUMBNIAIL {} {}'.format(photo_id, size))
            generate_thumbnail.delay(photo_id, size, fileformat)
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/photos/<int:photo_id>/', defaults={'size': None})
@app.route('/photos/<int:photo_id>/<string:size>')
def photo(photo_id, size):
    with sqlite3.connect(config.DATABASE_URL) as conn:
        cur = conn.cursor()
        row = cur.execute('SELECT * FROM photos WHERE id=?', (photo_id,)).fetchone()
    if not row:
        return render_template('404.html')

    photo_data = process_row(row)

    if size:
        try:
            photo_id = row[0]
            ext = row[1].split(".")[-1]
            resp = minio_client.get_object(bucket_name=config.MINIO_BUCKET, object_name=f"{photo_id}/{size}.{ext}")
            data = BytesIO(resp.read())
            resp.close()
            resp.release_conn()
            return send_file(data, mimetype='application/octet-stream', as_attachment=True, download_name=f"{size}_{row[1]}")
        except Exception as e:
            abort(404)

    else:
        return render_template('photo.html', photo_data=photo_data)
