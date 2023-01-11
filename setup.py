import redis
import os
import argparse

parser = argparse.ArgumentParser(description='Tech Co Simulation Setup.')
parser.add_argument('--redis-host', dest='redis_host', action='store', default="localhost", help='The redis hostname (default: localhost)')
parser.add_argument('--redis-port', dest='redis_port', action='store', default=6379, help='The redis port (default: 6379)')
parser.add_argument('--budget', dest='budget', action='store', default=30, help='The starting company budget (default: 30)')
args = parser.parse_args()

r = redis.Redis(host=args.redis_host, port=args.redis_port)

default_values = {
    "employees": 0,
    "money": args.budget,
    "customer_base": 0,
    "customer_happiness": 0,
    "tutorials": 0,
    "bugs_fixed": 0
}

r.mset(default_values)
print(r.keys("*"))