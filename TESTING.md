# CSEE 4119 Spring 2024, Class Project

## Team name: Blockchain Smoker

## Team members (name, GitHub username):

- Jane Lim - janelim0414
- Tattie Chitrakorn - tchitrakorn
- Karen Wang - karenswang
- Charlie Heus - Charlie-Heus

## Blockchain Testing

Please see `src/test_blockchain.py` for full test suites. To run this file, please use the following command: `python -m coverage run -m unittest --verbose`

### Test Class: Block

#### test_genesis_block - PASSED

Test that the first block in the chain is a Genesis block, marked by 'Genesis' as data.

#### test_create_valid_block - PASSED

Test that a new block can be created using the hash of the last known block in the chain.

#### test_create_invalid_block - PASSED

Test that a new block can be created using the an invalid hash (e.g., random string). Note that this works as intended. Blocks with invalid hash can be created but cannot be added to an existing chain (to be tested below).

### Test Class: Blockchain

#### test_add_valid_block - PASSED

Test that a valid block can be added to an existing blockchain. Confirm by checking the data of the last block of the chain.

#### test_add_invalid_block_invalid_hash - PASSED

Test that a new block with invalid hash cannot be added to an existing blockchain. Confirm by checking the data of the last block of the chain (still a Genesis block).

#### test_add_invalid_block_invalid_difficulty - PASSED

Test that a new block with invalid hash difficulty (i.e., '0001' instead of '0000') cannot be added to an existing blockchain. Confirm by checking the data of the last block of the chain (still a Genesis block).

#### test_add_invalid_block_partial_invalid_hash - PASSED

Test that a new block with partially valid hash (i.e., beginning with the correct difficulty level but otherwise a random string) cannot be added to an existing blockchain. Confirm by checking the data of the last block of the chain (still a Genesis block).
