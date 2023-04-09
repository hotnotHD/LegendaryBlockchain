from flask import Flask, request
import requests
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

def block_to_dict(block):
    dict_ = {
        'index': block.index,
        'prev_hash': block.prev_hash,
        'hash': block.hash,
        'data': block.data,
        'nonce': block.nonce,
        'time': block.time
    }
    return dict_


app = Flask(__name__)

blk = Blockchain()

url_l = "http://localhost"


@app.route('/mine', methods=['POST'])
def mine():
    next_block = blk.new_block(int(blk.blocks[-1]['index']) + 1, blk.blocks[-1]['hash'])
    next_block_dict = block_to_dict(next_block)
    if int(next_block_dict.get('index')) == int(blk.blocks[-1]['index']) + 1:
        blk.add_block(next_block_dict)

        for i in blk.addresses:
            url = url_l + ":" + str(i) + "/new_block"
            requests.post(url, params=next_block_dict, data=str(blk.address))
    return "Done"


@app.route('/new_block', methods=['POST'])
def new_block():
    req = request
    dat = req.args.to_dict()
    ar_index = int(dat.get('index'))
    ar_time = float(dat.get('time'))
    prev_hash = dat.get('prev_hash')

    if ar_index == len(blk.blocks) and ar_index == int(blk.blocks[-1]['index']) + 1 and prev_hash == blk.blocks[-1]['hash']:
        blk.add_block(dat)
    elif ar_index > len(blk.blocks):
        i = random.choice(blk.addresses)
        url = url_l + ":" + str(i) + "/chain_send"
        requests.post(url, params={"address": blk.address})
    elif ar_time < float(blk.blocks[ar_index]['time']) and prev_hash == blk.blocks[ar_index]['hash']:
        blk.chain_clean(ar_index)
        blk.add_block(dat)
    else:
        adr = req.data.decode("UTF-8")
        url = url_l + ":" + str(adr) + "/chain_actual"
        requests.post(url, params={"chain": str(blk.blocks)})

    return "Done"


@app.route('/chain_actual', methods=['POST'])
def chain_actual():
    dat = request.args.to_dict().get("chain")
    blk.new_chain(dat)

    return "accept"


@app.route('/chain_send', methods=['POST', 'GET'])
def chain_send():
    dat = request.args.to_dict().get("address")
    url = url_l + ":" + str(dat) + "/chain_actual"
    requests.post(url, params={"chain": str(blk.blocks)})

    return "sended"


@app.route('/start_mine', methods=['POST', 'GET'])
def start_mine():
    genesis_block = blk.new_block(0, "GENESIS")

    genesis_dict = block_to_dict(genesis_block)
    blk.add_block(genesis_dict)

    for i in blk.addresses:
        url = url_l + ":" + str(i) + "/start_slave"
        requests.post(url, params=genesis_dict)
    return "Lest`s begin"


@app.route('/start_slave', methods=['POST'])
def start_slave():
    dat = request.args.to_dict()
    blk.add_block(dat)
    return "rec"


@app.route('/data')
def data():
    return f'{blk.blocks}'
