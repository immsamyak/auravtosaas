import redis
import random

r = redis.Redis(host='127.0.0.1', port=6379, db=1)
r.flushdb()

# Simulate some cache hits and misses
for _ in range(100):
    r.set(f"key_{random.randint(1, 100)}", "value")

for _ in range(500):
    r.get(f"key_{random.randint(1, 150)}")
