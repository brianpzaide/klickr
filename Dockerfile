FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
RUN mkdir /app/data
RUN mkdir /app/data/klickr
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000
ENV FLASK_DEBUG=true
ENV FLASK_ENV=development

CMD ["python", "run.py"]
