import mmh3
from bitarray import bitarray


class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, item):
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            self.bit_array[digest] = 1

    def check(self, item):
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size

            if self.bit_array[digest] == 0:
                return False

        return True


# Change size to experiment with false positives
bf = BloomFilter(size=50, hash_count=3)

items = ["apple", "banana", "grapes"]

for item in items:
    bf.add(item)

test = ["apple", "banana", "mango", "orange"]

for item in test:
    print(item, "->", bf.check(item))