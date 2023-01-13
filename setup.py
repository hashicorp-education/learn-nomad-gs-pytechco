import redis
import os
import argparse

# parser = argparse.ArgumentParser(description='Tech Co Simulation Setup.')
# parser.add_argument('--redis-host', dest='redis_host', action='store', default='localhost', help='The redis hostname (default: localhost)')
# parser.add_argument('--redis-port', dest='redis_port', action='store', default=6379, help='The redis port (default: 6379)')
# parser.add_argument('--budget', dest='budget', action='store', default=30, help='The starting company budget (default: 30)')
# args = parser.parse_args()

redis_host = os.getenv('REDIS_HOST', default='localhost')
redis_port = os.getenv('REDIS_PORT', default=6379)
budget = os.getenv('PTC_BUDGET', default=30)

r = redis.Redis(host=redis_host, port=redis_port)

default_values = {
    'employees': 0,
    'money': budget,
    'customer_base': 0,
    'customer_happiness': 0,
    'tutorials': 0,
    'bugs_fixed': 0
}

r.flushall()
r.mset(default_values)
print(r.keys('*'))