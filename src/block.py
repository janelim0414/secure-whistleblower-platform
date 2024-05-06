import datetime
import hashlib
from pprint import pprint

class Block:
    def __init__(self, block_number, data, prev_hash, curr_hash=None, nonce=None, timestamp=None):
        """
        initialize a block with relevant fields 
        
        parameters:
        block_number - int
        data - str
        prev_hash - str
        curr_hash - str
        nonce - int
        timestamp - datetime 
        """
        self.block_number = block_number
        self.data = data
        self.prev_hash = prev_hash
        self.curr_hash = curr_hash
        self.nonce = nonce
        self.timestamp = datetime.datetime.now()
    
    def __str__(self):
        return f"Block Number: {self.block_number}, Data: {self.data}, Hash: {self.curr_hash}, Prev Hash: {self.prev_hash}, Nonce: {self.nonce}, craeted at: {self.timestamp}"
    
    def print_block(self):
        """
        a debugging function that print the whole block
        """
        pprint(vars(self))

    def get_hash(self, nonce):
        """
        compute and return a hash of current block given the data, prev_hash, and nonce value

        arguments:
        nonce - value representing nonce value (int)

        returns: (str) hash of data, previous hash, and nonce 
        """
        sha = hashlib.sha256()
        sha.update(str(self.data).encode('utf-8') + str(self.prev_hash).encode('utf-8') + str(nonce).encode('utf-8')) 
        return sha.hexdigest() 

    def mine(self, hash_requirement):
        """
        given all the information, find nonce that makes curr_hash valid based on the hash_difficulty provided

        arguments:
        hash_requirement - value representing hash difficulty (str)

        returns: (str) current hash value after correct nonce and hash found
        """
        temp_nonce = 0
        temp_hash = self.get_hash(temp_nonce)
        # finding a valid hash by incrementing a nonce value by one
        while temp_hash[:len(hash_requirement)] != hash_requirement:
            temp_nonce += 1
            temp_hash = self.get_hash(temp_nonce)
        # once the correct nonce and hash are found, store that in the block
        self.nonce = temp_nonce
        self.curr_hash = temp_hash
        return self.curr_hash
            
    def to_dict(self):
        return {
            'block_number': self.block_number,
            'data': self.data,
            'prev_hash': self.prev_hash,
            'timestamp': self.timestamp
        }