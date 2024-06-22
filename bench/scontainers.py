from random import randrange
from bisect import insort
from vectorish import vector
from sortedcontainers import SortedList
coll = SortedList()
N = 1000000
for _ in range(N):
    coll.add(randrange(100000))
assert len(coll) == N
