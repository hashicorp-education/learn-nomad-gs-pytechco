FROM python:alpine
LABEL org.opencontainers.image.source=https://github.com/hashicorp-education/learn-nomad-gs-pytechco

WORKDIR /usr/src/app

COPY webviewer.py index.html .
COPY requirements-web.txt .

RUN pip install --no-cache-dir -r requirements-web.txt

ENTRYPOINT ["python", "./webviewer.py"]