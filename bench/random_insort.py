from random import randrange
from bisect import insort
from vectorish import vector
coll = list()
N = 1000000
for _ in range(N):
    insort(coll, randrange(100000))
assert len(coll) == N