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

## P2P Testing and Results

#### Tracker functionality
<Peer joining>
$ python3 p2p.py 55555 10.128.0.5 0 (Tracker)
Internal IP: 10.128.0.5
Server listening on port: 55555

Client connected from: ('10.128.0.6', 60362)

New peer joined: 10.128.0.6

Updated list of peers sent to <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.128.0.5', 55555), raddr=('10.128.0.6', 60362)>: ['10.128.0.6']
Client connected from: ('10.128.0.7', 51136)

New peer joined: 10.128.0.7

Updated list of peers sent to <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.128.0.5', 55555), raddr=('10.128.0.6', 60362)>: ['10.128.0.6', '10.128.0.7']
Updated list of peers sent to <socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.128.0.5', 55555), raddr=('10.128.0.7', 51136)>: ['10.128.0.6', '10.128.0.7']
Client connected from: ('10.128.0.8', 60830)

New peer joined: 10.128.0.8

Updated list of peers sent to <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.128.0.5', 55555), raddr=('10.128.0.6', 60362)>: ['10.128.0.6', '10.128.0.7', '10.128.0.8']
Updated list of peers sent to <socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.128.0.5', 55555), raddr=('10.128.0.7', 51136)>: ['10.128.0.6', '10.128.0.7', '10.128.0.8']
Updated list of peers sent to <socket.socket fd=6, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.128.0.5', 55555), raddr=('10.128.0.8', 60830)>: ['10.128.0.6', '10.128.0.7', '10.128.0.8']

$ python3 p2p.py 55555 10.128.0.5 0 (Peer 1)
Internal IP: 10.128.0.6
list of peers: []
received from tracker: ['10.128.0.6']
updated list of peers: []
list of peers: []

received from tracker: ['10.128.0.6', '10.128.0.7']
send channel connected from: 10.128.0.7
Client connected from: ('10.128.0.7', 56716)
list of peers: ['10.128.0.7']

Client connected from: ('10.128.0.8', 34162)
received from tracker: ['10.128.0.6', '10.128.0.7', '10.128.0.8']
send channel connected from: 10.128.0.8

$ python3 p2p.py 55555 10.128.0.5 0 (Peer 2)
Internal IP: 10.128.0.7
list of peers: []
received from tracker: ['10.128.0.6', '10.128.0.7']
send channel connected from: 10.128.0.6
Client connected from: ('10.128.0.6', 59608)
updated list of peers: ['10.128.0.6']

list of peers: ['10.128.0.6']
received from tracker: ['10.128.0.6', '10.128.0.7', '10.128.0.8']
Client connected from: ('10.128.0.8', 60152)
send channel connected from: 10.128.0.8
updated list of peers: ['10.128.0.6', '10.128.0.8']

$ python3 p2p.py 55555 10.128.0.5 0 (Peer 3)
Internal IP: 10.128.0.8
list of peers: []
received from tracker: ['10.128.0.6', '10.128.0.7', '10.128.0.8']
send channel connected from: 10.128.0.6

send channel connected from: 10.128.0.7
Client connected from: ('10.128.0.6', 54576)
Client connected from: ('10.128.0.7', 55358)
updated list of peers: ['10.128.0.6', '10.128.0.7']
list of peers: ['10.128.0.6', '10.128.0.7']

<Peer leaving>
$ python3 p2p.py 55555 10.128.0.5 0 (Tracker, cont.)
Internal IP: 10.128.0.5
Server listening on port: 55555
=======================================================
Peer left: 10.128.0.6

Updated list of peers sent to <socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.128.0.5', 55555), raddr=('10.128.0.7', 51136)>: ['10.128.0.7', '10.128.0.8']
Updated list of peers sent to <socket.socket fd=6, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.128.0.5', 55555), raddr=('10.128.0.8', 60830)>: ['10.128.0.7', '10.128.0.8']
Peer left: 10.128.0.7

Updated list of peers sent to <socket.socket fd=6, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.128.0.5', 55555), raddr=('10.128.0.8', 60830)>: ['10.128.0.8']

$ python3 p2p.py 55555 10.128.0.5 0 (Peer 2, cont.)
Internal IP: 10.128.0.7
=======================================================
list of peers: ['10.128.0.6', '10.128.0.8']
Client disconnected: <socket.socket [closed] fd=-1, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0>
received from tracker: ['10.128.0.7', '10.128.0.8']
updated list of peers: ['10.128.0.8']

$ python3 p2p.py 55555 10.128.0.5 0 (Peer 3, cont.)
Internal IP: 10.128.0.8
=======================================================
Client disconnected: <socket.socket [closed] fd=-1, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0>
list of peers: ['10.128.0.6', '10.128.0.7']
received from tracker: ['10.128.0.7', '10.128.0.8']
updated list of peers: ['10.128.0.7']

#### Peer functionality
<Sending and receiving blocks>
Block data = 'block 1 data from 10.128.0.7'
Block added to = '10.128.0.7'

$ python3 p2p.py 55555 10.128.0.5 0
Internal IP: 10.128.0.6
===========================================
dict data sent: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': datetime.datetime(2024, 5, 7, 15, 53, 43, 5664)}], 'block_number': 1, 'most_recent_hash': '0', 'hash_requirement': '0000'}
chain received: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': '2024-05-07T15:53:47.034187'}], 'block_number': 1, 'most_recent_hash': '0', 'hash_requirement': '0000'}