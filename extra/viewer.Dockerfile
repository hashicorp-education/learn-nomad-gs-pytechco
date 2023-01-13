FROM python:alpine

WORKDIR /usr/src/app

COPY viewer.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "./viewer.py"]