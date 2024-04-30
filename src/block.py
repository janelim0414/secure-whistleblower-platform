import datetime
import hashlib
from pprint import pprint

class Block:
    def __init__(self, block_number, data, prev_hash):
        """
        initialize a block with relevant fields 
        
        parameters:
        block_number - 
        data - 
        prev_hash - 
        curr_hash - 
        nonce - 
        timestamp - 
        """
        self.block_number = block_number
        self.data = data
        self.prev_hash = prev_hash
        self.curr_hash = None
        self.nonce = None
        self.timestamp = datetime.datetime.now()
    
    def print_block(self):
        """
        a debugging function that print the whole block
        """
        pprint(vars(self))

    def get_hash(self, nonce):
        """
        compute and return a hash of current block given the data, prev_hash, and nonce value
        """
        sha = hashlib.sha256()
        sha.update(str(self.data).encode('utf-8') + str(self.prev_hash).encode('utf-8') + str(nonce).encode('utf-8')) 
        return sha.hexdigest() 

    def mine(self, hash_requirement):
        """
        given all the information, find nonce that makes curr_hash valid based on the hash_difficulty provided

        parameters:
        hash_requirement
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
            
