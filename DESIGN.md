# BlockchainSmoker DESIGN.md

## Blockchain Design
### Block class
#### Overview:
* Individual block object
#### Fields:
* block_number
* nonce
* data
* prev_hash
* curr_hash
* timestamp
#### Methods
##### init(block_number, data, prev_hash)
* Initialize a block given data and block_number
##### mine(hash_difficulty)
* Given all the information, find nonce that makes curr_hash valid based on the hash_difficulty provided

### Blockchain class
#### Overview:
* Hold all the blocks
#### Fields:
* chain - a list of Block objects
* block_num - current block number
* most_recent_hash - the most recent hash value (for block validation)
* hash_difficulty - string of hashing condition (for block validation)
#### Methods
##### init() - initizes the chain
##### create_genesis_block()
* Create a dummy head for the block chain
##### create_block(prev_hash, data)
* Validate that prev_hash is valid and if so, create a new Block object and add it to the chain
##### get_chain()
* Return the whole chain
##### get_last_block()
* Return the last block in the chain

### Note
* In this architecture, P2P has to handle all broadcasting of blockchain data, including packaging block data into appropriate packet in bytes

## P2P Protocol
### Each node…
* Locally stores a blockchain and receives longest blockchain upon joining
* Periodically requests a list of all active nodes from tracker
* Creates a new block and sends it over TCP to all other nodes
* Receives a new block sent from the longest blockchain
### Tracker
* Keeps a list of addresses of all active nodes by periodically receiving/not receiving peers' addresses
### Special cases
#### Ensuring that every node has the correct copy of their local blockchain:
* Longest blockchain - only accept new block sent from the longest blockchain and newly joined peer is updated with the longest blockchain to avoid conflict
* Timestamps - use timestamps to see which was created first

## Demo Application - Secured Whistleblower Platform
* A platform for verified users to anonymously reach out to appropriate authorities to act on their behalf against the misconduct of certain organizations or individuals
* Only the parties of interest would be able to verify each other’s identities. This ensures both the privacy and validity of the information.


