import redis
import random

r = redis.Redis(host='64.227.167.223', port=6379, db=1, password='bx2Ee2Q8grqKcWfawRwCVoz8YKyQsqciijqsSmUIe1PDZIOnbbYj9liWJ2c6jQDp')
r.flushdb()

for _ in range(100):
    r.set(f"key_{random.randint(1, 100)}", "value")

for _ in range(500):
    r.get(f"key_{random.randint(1, 150)}")
