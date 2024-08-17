import logging

from klickr.app import app
from klickr.utils import setup_db

def setup_logger(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(message)s",
        datefmt="%H:%M:%S"
    )

def main():
    setup_logger(verbose=True)
    setup_db()
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
