from src.main import Block


test_block_gen = Block(0, "GENESIS")
test_block_next = Block(int(test_block_gen.index) + 1, test_block_gen.hash)

def test_block_hash_gen():
    assert test_block_gen.hash_gen()[-4:] == "0000"

def test_block_concat():
    assert test_block_gen.concat() == "0GENESIS" + test_block_gen.data + str(test_block_gen.nonce)

def test_block_index():
    assert int(test_block_gen.index) == 0

def test_block_prev_hash():
    assert test_block_gen.prev_hash == "GENESIS"

def test_block_hash():
    assert test_block_gen.hash[-4:] == "0000"

def test_block_index_2():
    assert int(test_block_next.index) == int(test_block_gen.index) + 1
    assert int(test_block_next.index) == 1

def test_block_hash_2():
    assert test_block_next.hash[-4:] == "0000"

def test_block_prev_hash_2():
    assert test_block_next.prev_hash == test_block_gen.hash

def random_data():
    assert test_block_gen.data != test_block_next.data

def test_time():
    assert test_block_gen.time < test_block_next.time
