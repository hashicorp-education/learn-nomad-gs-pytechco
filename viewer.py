import redis
import time
import signal
import sys
import os
import argparse

parser = argparse.ArgumentParser(description='PyTechCo Simulator viewer app.')
parser.add_argument('--redis-host', dest='redis_host', action='store', default="localhost", help='The redis hostname (default: localhost)')
parser.add_argument('--redis-port', dest='redis_port', action='store', default=6379, help='The redis port (default: 6379)')
args = parser.parse_args()

def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

r = redis.Redis(host=args.redis_host, port=args.redis_port)

while True:
    os.system("clear")
    for key in r.scan_iter("*"):
        print(f"{key.decode()} = {r.get(key).decode()} ")
    time.sleep(1)