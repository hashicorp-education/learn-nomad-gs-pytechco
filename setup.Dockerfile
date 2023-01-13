FROM python:alpine

WORKDIR /usr/src/app

COPY setup.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "./setup.py"]