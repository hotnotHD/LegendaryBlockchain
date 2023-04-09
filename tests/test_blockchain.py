from src.main import Blockchain
from src.main import block_to_dict

blockchain = Blockchain()

def test_to_dict():
    new_blk = blockchain.new_block(0, "GENESIS")

    blk_dict = block_to_dict(new_blk)

    assert new_blk.index == blk_dict.get("index")
    assert new_blk.hash == blk_dict.get("hash")
    assert new_blk.data == blk_dict.get("data")
    assert new_blk.nonce == blk_dict.get("nonce")
    assert new_blk.time == blk_dict.get("time")
    assert new_blk.prev_hash == blk_dict.get("prev_hash")

def test_new_block():
    new_blk = blockchain.new_block(0, "GENESIS")
    assert new_blk.index == "0"
    assert new_blk.prev_hash == "GENESIS"

def test_add_new_block():
    new_blk = blockchain.new_block(0, "GENESIS")
    blockchain.add_block(block_to_dict(new_blk))
    assert blockchain.blocks[0] == block_to_dict(new_blk)
    assert len(blockchain.blocks) == 1

def test_chain_clean():
    blockchain.blocks = []
    new_blk = blockchain.new_block(0, "GENESIS")
    blockchain.add_block(block_to_dict(new_blk))
    new_blk_2 = blockchain.new_block(1, new_blk.hash)
    blockchain.add_block(block_to_dict(new_blk_2))
    index = blockchain.blocks[1]['index']
    assert index == "1"
    assert len(blockchain.blocks) == 2

    blockchain.chain_clean(1)
    assert len(blockchain.blocks) == 1

    blockchain.chain_clean(0)
    assert len(blockchain.blocks) == 0

def test_new_chain():
    dat = "[{'index': '0', 'prev_hash': 'GENESIS', 'hash': '9b21987aacc0bb37a904bc5672dcb9c839b5d890e44192a383695a64f29a0000', 'data': 'fuijccborrshlkhilmbxvdvjzfdkyyegvembfyqgkpwtfaohjxddvmcaxrqjeegfnyfdclfywarzcpkndcuoaefbbruylqlewhawouzwzlbdebneekpkrayqkyhgcwwrqnfbkpfezywljxrwtqxnmdfoupctustfkisflhgbdykdslrqzuedltudgotvfnpdeduinmzebbepfyobymfocitnmjvbexnmoqyewwexpligqbogivlmoolgzducjpzf', 'nounce': '285693', 'time': '1681043218.6392334'}]"
    blockchain.new_chain(dat)
    dat_dict = {
        'index': '0', 'prev_hash': 'GENESIS',
        'hash': '9b21987aacc0bb37a904bc5672dcb9c839b5d890e44192a383695a64f29a0000',
        'data': 'fuijccborrshlkhilmbxvdvjzfdkyyegvembfyqgkpwtfaohjxddvmcaxrqjeegfnyfdclfywarzcpkndcuoaefbbruylqlewhawouzwzlbdebneekpkrayqkyhgcwwrqnfbkpfezywljxrwtqxnmdfoupctustfkisflhgbdykdslrqzuedltudgotvfnpdeduinmzebbepfyobymfocitnmjvbexnmoqyewwexpligqbogivlmoolgzducjpzf',
        'nounce': '285693',
        'time': '1681043218.6392334'
    }
    assert blockchain.blocks[0] == dat_dict

