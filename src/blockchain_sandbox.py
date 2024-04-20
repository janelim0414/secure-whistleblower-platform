from blockchain import Blockchain
from block import Block
from copy import copy

if __name__ == '__main__':
    """
    this sandbox provides an example of how Block and Blockchain classes can be used
    """

    print('-- Node 1 --')
    # Each node needs to initialize a Blockchain object
    # All blocks will be stored in-memory in this object
    chain_1 = Blockchain()

    # Note that the first block is always a genesis block (sort of like a dummy head)
    last_block = chain_1.get_last_block()
    last_block.print_block()
    
    # A new block can be added by to a Blockchain object
    # It's important to provide prev_hash to verify that this new block is valid
    # This is not a problem if a node adds a new block to its own local blockchain because they can simply get prev_hash from last_block
    new_block = Block(last_block.block_number + 1, 'block 1 data', last_block.prev_hash)
    # After a block is created, it needs to be mined to find the right nonce and curr_hash
    # mine() takes a difficulty level, which in this case is a string of 4 zeros. This is the condition for a valid hash.
    # mine() also returns the new hash of the block. This will be used to verifiy that a block is valid when adding it to a blockchain
    new_block_hash = new_block.mine('0000')
    try:
        # This is how a block can be added to a blockchain
        chain_1.add_block(new_block, new_block_hash)
    except Exception as e:
        print(e)

    # Note that the block is successfully created 
    chain_1.get_last_block().print_block()
    print('-- End of Node 1 --')

    print('-- Node 2 --')
    # Now, let's imagine that a different node wants to add a new block to its local blockchain 
    # For simplicity, I will clone the second chain to get a full copy of chain_1
    chain_2 = copy(chain_1)
    chain_2_last_block = chain_2.get_last_block()

    # If this node wants to add an INVALID block to chain_2 (aka invalid prev_hash), an error will return and no new block will be added
    invalid_block = Block(chain_2_last_block.block_number + 1, 'block 2 data invalid 1', 'invalid hash')
    invalid_block_hash = invalid_block.mine('0000')
    try:
        chain_2.add_block(invalid_block, invalid_block_hash)
        print('Valid block added')
    except Exception as e:
        print('Invalid Block error :' ,e)

    # Another case of INVALID block is when the curr hash of a block does not satisfy the difficulty or the hash does not equal to actual block hash (aka random value)
    invalid_block_2 = Block(chain_2_last_block.block_number + 1, 'block 2 data invalid 2', chain_2_last_block.curr_hash)
    invalid_block_2_hash = invalid_block.mine('0001')
    try:
        chain_2.add_block(invalid_block, invalid_block_2_hash)
        print('Valid block added')
    except Exception as e:
        print('Invalid Block error :' , e)
    
    invalid_block_3 = Block(chain_2_last_block.block_number + 1, 'block 2 data invalid 3', chain_2_last_block.curr_hash)
    invalid_block_3_hash = '0000d2s013'
    try:
        chain_2.add_block(invalid_block, invalid_block_3_hash)
        print('Valid block added')
    except Exception as e:
        print('Invalid Block error :' , e)

    # Note here that the latest block is still 'block 1 data' because the previous additions were invalid
    chain_2.get_last_block().print_block()

    # However, let's imagine that Node 2 receives a valid block from Node 1 over the TCP
    # Now chain 2 should be able to add a new block beceause Blockchain object will first verfiy that the hash is valid
    new_block = Block(chain_1.get_last_block().block_number + 1, 'block 2 data received from chain 1', chain_1.get_last_block().curr_hash)
    new_block_hash = new_block.mine('0000')
    try:
        chain_2.add_block(new_block, new_block_hash)
        print('Valid block added')
    except Exception as e:
        print(e)

    # Note that the last block is now updated to 'block 2 data received from chain 1'
    chain_2.print_chain()
    print('-- End of Node 2 --')
