"""
Our trie implementation
"""

_SENTINEL = object()


class Trie(dict):
    "A trie"

    def __init__(self):
        super(Trie, self).__init__()

    def insert(self, key, value):
        "Inserts a key-value pair into the trie"
        trie = self
        for char in key:
            if char not in trie:
                trie[char] = {}
            trie = trie[char]
        trie[_SENTINEL] = value

    def iterate(self, key):
        "Yields all values on all nodes for a key"
        trie = self
        for char in key:
            if _SENTINEL in trie:
                yield trie[_SENTINEL]
            if char in trie:
                trie = trie[char]
            else:
                break
