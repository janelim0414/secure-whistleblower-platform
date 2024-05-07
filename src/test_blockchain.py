import unittest
from block import Block
from blockchain import Blockchain


class TestBlock(unittest.TestCase):
    def test_genesis_block(self):
        chain = Blockchain()
        actual = chain.get_last_block().data
        expected = 'Genesis'
        self.assertEqual(actual, expected)

    def test_create_valid_block(self):
        chain = Blockchain()
        new_block = Block(chain.get_last_block().block_number + 1, 'new data', chain.get_last_block().curr_hash)
        actual = new_block.data
        expected = 'new data'
        self.assertEqual(actual, expected)

    def test_create_invalid_block(self):
        # invalid block can be created but it cannot be added to an exisiting chain
        chain = Blockchain()
        new_block = Block(chain.get_last_block().block_number + 1, 'new data', 'invalid hash')
        actual = new_block.data
        expected = 'new data'
        self.assertEqual(actual, expected)

class TestBlockchain(unittest.TestCase):
    def test_add_valid_block(self):
        chain = Blockchain()
        new_block = Block(chain.get_last_block().block_number + 1, 'new data', chain.get_last_block().curr_hash)
        new_block_hash = new_block.mine('0000')
        chain.add_block(new_block, new_block_hash)
        actual = chain.get_last_block().data
        expected = 'new data'
        self.assertEqual(actual, expected)

    def test_add_invalid_block_invalid_hash(self):
        chain = Blockchain()
        new_block = Block(chain.get_last_block().block_number + 1, 'new data', 'invalid hash')
        new_block_hash = new_block.mine('0000')
        try:
            chain.add_block(new_block, new_block_hash)
        except Exception as e:
            pass
        actual = chain.get_last_block().data
        expected = 'Genesis'
        self.assertEqual(actual, expected)

    def test_add_invalid_block_invalid_difficulty(self):
        chain = Blockchain()
        new_block = Block(chain.get_last_block().block_number + 1, 'new data', 'invalid hash')
        new_block_hash = new_block.mine('0001')  # expected difficulty is '0000'
        try:
            chain.add_block(new_block, new_block_hash)
        except Exception as e:
            pass
        actual = chain.get_last_block().data
        expected = 'Genesis'
        self.assertEqual(actual, expected)

    def test_add_invalid_block_partial_invalid_hash(self):
        chain = Blockchain()
        new_block = Block(chain.get_last_block().block_number + 1, 'new data', 'invalid hash')
        new_block_hash = '0000d2s013'  # satisfied difficulty level but actually a random value 
        try:
            chain.add_block(new_block, new_block_hash)
        except Exception as e:
            pass
        actual = chain.get_last_block().data
        expected = 'Genesis'
        self.assertEqual(actual, expected)


