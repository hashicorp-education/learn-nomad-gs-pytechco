FROM python:alpine

WORKDIR /usr/src/app

COPY webviewer.py index.html .
COPY requirements-web.txt .

RUN pip install --no-cache-dir -r requirements-web.txt

ENTRYPOINT ["python", "./webviewer.py"]