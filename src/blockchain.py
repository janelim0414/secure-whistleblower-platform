from block import Block

class Blockchain:
    def __init__(self, chain=None):
        """
        initialize a blockchain
        
        parameters:
        chain - 
        block_number - 
        most_recent_hash - 
        hash_requirement - 
        """
        if chain:
            self.chain = chain
        else:
            self.chain = [self.create_genesis_block()]
        self.block_number = 1
        self.most_recent_hash = '0'
        self.hash_requirement = '0000'  # a hash is valid only if the first four characters exactly match the hash_difficulty

    def create_genesis_block(self):
        """
        create a dummy head for the block chain
        """
        return Block(1, 'Genesis', '0')
    
    def valid_proof(self, new_block, new_block_hash):
        return new_block_hash.startswith(self.hash_requirement) and new_block_hash == new_block.get_hash(new_block.nonce)
    
    def add_block(self, new_block, new_block_hash):
        """
        validate that the new block's prev_hash is valid and if so, create a new Block object and add it to the chain
        """
        if new_block.prev_hash == self.most_recent_hash and self.valid_proof(new_block, new_block_hash):
            self.block_number += 1
            self.chain.append(new_block)
            self.most_recent_hash = new_block.curr_hash
            return self.most_recent_hash
        else:
            raise Exception('Invalid prev_hash')

    def get_chain(self):
        """
        return the whole chain        
        """
        return self.chain
    
    def get_last_block(self):
        """
        return the last block in the chain       
        """
        return self.chain[-1]
    
    def print_chain(self):
        """
        a debugging function that print the whole chain
        """
        for block in self.get_chain():
            block.print_block()