FROM python:alpine
LABEL org.opencontainers.image.source=https://github.com/hashicorp-education/learn-nomad-gs-pytechco

WORKDIR /usr/src/app

COPY setup.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "./setup.py"]