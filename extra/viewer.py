import redis
import time
import signal
import sys
import os
import argparse
import json

parser = argparse.ArgumentParser(description='PyTechCo Simulator viewer app.')
parser.add_argument('--redis-host', dest='redis_host', action='store', default="localhost", help='The redis hostname (default: localhost)')
parser.add_argument('--redis-port', dest='redis_port', action='store', default=6379, help='The redis port (default: 6379)')
args = parser.parse_args()

def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

r = redis.Redis(host=args.redis_host, port=args.redis_port)

def get_stats_from_db(results):
    output = ""
    for key in r.scan_iter("*"):
        if not key.decode().startswith("employee-"):
            output += f"{key.decode(): <25} {r.get(key).decode()}\n"
    return output

def get_employees_online_from_db(results):
    output = ""
    for key in r.scan_iter("*"):
        if key.decode().startswith("employee-"):
            attr = json.loads(r.get(key).decode())
            status = attr.get("status")
            if status == "online":
                output += f"Employee {attr.get('id')} is a {attr.get('title')} and online!\nThey're working on {attr.get('primary_task')} and {attr.get('secondary_task')}!\n\n"
    return output

while True:
    os.system("clear")
    results = r.scan_iter("*")
    print(get_stats_from_db(results))
    print(get_employees_online_from_db(results))
    time.sleep(1)