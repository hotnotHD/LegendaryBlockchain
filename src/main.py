import string
import random
from hashlib import sha256
import json
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

class Blockchain:
    def __init__(self):
        self.blocks = []
        self.address = 0
        self.addresses = [5000, 5001, 5002]

    def new_block(self, index, prev_hash):
        return Block(index, prev_hash)

    def add_block(self, block):
        self.blocks.append(block)

    def chain_clean(self, index):
        while len(self.blocks) > index:
            self.blocks.pop()

    def new_chain(self, dat):
        dat = dat[1:-1]
        dat = dat.split("}, {")
        self.blocks = []
        for i in dat:
            i = i.strip("{")
            i = i.strip("}")
            i = "{" + i + "}"
            i = i.replace("\'", "\"")
            self.add_block(json.loads(i))
