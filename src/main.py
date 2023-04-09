import string
import random
from hashlib import sha256
import time


class Block:
    def __init__(self, index, prev_hash):
        self.index = str(index)
        self.prev_hash = prev_hash

        self.data = ""
        self.nonce = "0"

        self.data = ''.join(random.choice(string.ascii_lowercase) for _ in range(256))
        self.hash = self.hash_gen()

        self.time = str(time.time())

    def concat(self):
        return str(self.index) + self.prev_hash + self.data + str(self.nonce)

    def hash_gen(self):
        hash_ = sha256(self.concat().encode('utf-8'))
        while hash_.hexdigest()[-4:] != "0000":
            self.nonce = str(int(self.nonce) + random.randint(1, 10))
            hash_ = sha256(self.concat().encode('utf-8'))
        return hash_.hexdigest()
