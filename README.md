# Klickr
Klickr is a miniscule clone of Flickr, an image-sharing app. This project was created for learning and practice purposes. Klickr uses the following technologies:
- *Flask*: For serving web requests (upload, download, list images).
- *Minio*: For storing images in a private S3-compatible object storage.
- *Celery*: For processing images, such as generating thumbnails and resizing images.
- *Redis*: As a message broker for the Celery worker.
- *Docker Compose*: For orchestrating all these services.

Below are the key steps I followed to build this project:
### Steps to Create the Project:

1. **Set Up a Basic Flask Application**:
   - Created a simple "Hello, World!" Flask application.
   - Ensured that the Flask app could connect to the Minio server upon startup.
   - Integrated an SQLite3 database, using a `schema.sql` file to create necessary tables.

2. **Implement Core Endpoints**:
   - Developed Flask endpoints for users to upload, download, and list images.

3. **Integrate Celery for Asynchronous Image Processing**:
   - Created a Celery task that automatically generates thumbnails and resizes images upon upload.
   - Configured the Celery worker to use Redis as the message broker.
   - Uploaded processed images (thumbnails and resized versions) back to the Minio server.
  
### Acknowledgments

The idea for this project came from the [Klickr](https://github.com/pipalacademy/klickr) by [Pipal Academy](https://pipal.in/). This project has been updated and modified to use Minio (instead of S3) and Celery (instead of RQ). The UI (HTML files) remains unchanged, as the main focus for working on this project was backend development.

### Getting Started

To build this project yourself, you can start with the original project from [Pipal Academy](https://github.com/pipalacademy/klickr). Follow the instructions provided in the original repository, and then modify it by integrating Minio (instead of S3) and Celery (instead of RQ) as I have done.

