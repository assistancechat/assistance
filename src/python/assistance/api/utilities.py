# Based on code at
# https://www.geeksforgeeks.org/lru-cache-in-python-using-ordereddict/

from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def __getitem__(self, key: int) -> int:
        result = self.cache[key]
        self.cache.move_to_end(key)

        return result

    def __setitem__(self, key: int, value: int) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
