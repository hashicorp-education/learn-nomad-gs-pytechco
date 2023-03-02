import redis
import os
import argparse

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