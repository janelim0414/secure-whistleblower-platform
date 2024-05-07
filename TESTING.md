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

#### Tracker functionality: Peer joining

Tracker

```
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
```

Peer 1

```
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
```

Peer 2

```
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
```

Peer 3

```
Internal IP: 10.128.0.8
list of peers: []
received from tracker: ['10.128.0.6', '10.128.0.7', '10.128.0.8']
send channel connected from: 10.128.0.6

send channel connected from: 10.128.0.7
Client connected from: ('10.128.0.6', 54576)
Client connected from: ('10.128.0.7', 55358)
updated list of peers: ['10.128.0.6', '10.128.0.7']
list of peers: ['10.128.0.6', '10.128.0.7']
```

#### Explanation 
1. Peers are able to receive updates from its trackers
2. Tracker is able to detect when any peer enters the network

#### Tracker functionality: Peer leaving
Tracker (cont.)

```
Internal IP: 10.128.0.5
Server listening on port: 55555
==============================================================================================
Peer left: 10.128.0.6

Updated list of peers sent to <socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.128.0.5', 55555), raddr=('10.128.0.7', 51136)>: ['10.128.0.7', '10.128.0.8']
Updated list of peers sent to <socket.socket fd=6, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.128.0.5', 55555), raddr=('10.128.0.8', 60830)>: ['10.128.0.7', '10.128.0.8']
Peer left: 10.128.0.7

Updated list of peers sent to <socket.socket fd=6, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.128.0.5', 55555), raddr=('10.128.0.8', 60830)>: ['10.128.0.8']
```

Peer 2 (cont.)

```
Internal IP: 10.128.0.7
================================================================================================
list of peers: ['10.128.0.6', '10.128.0.8']
Client disconnected: <socket.socket [closed] fd=-1, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0>
received from tracker: ['10.128.0.7', '10.128.0.8']
updated list of peers: ['10.128.0.8']
```

Peer 3 (cont.)

```
Internal IP: 10.128.0.8
==================================================================================================
Client disconnected: <socket.socket [closed] fd=-1, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0>
list of peers: ['10.128.0.6', '10.128.0.7']
received from tracker: ['10.128.0.7', '10.128.0.8']
updated list of peers: ['10.128.0.7']
```

#### Explanation 
1. Peers are able to receive updates from its trackers
2. Tracker is able to detect when any peer leaves the network

#### Peer functionality: Sending and receiving blocks
Block data = 'block 1 data from 10.128.0.7'
Block added to = '10.128.0.7'

Peer 1

```
Internal IP: 10.128.0.6
Expected behavior: send its chain to newly joined peers (first 10.128.0.7 then 10.128.0.8), receive new block from 10.128.0.7, add to its chain then send to 10.128.0.8
=====================================================================================================
send channel connected from: 10.128.0.7
dict data sent: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': datetime.datetime(2024, 5, 7, 15, 53, 43, 5664)}], 'block_number': 1, 'most_recent_hash': '0', 'hash_requirement': '0000'}

Client connected from: ('10.128.0.7', 59256)
chain received: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': '2024-05-07T15:53:47.034187'}], 'block_number': 1, 'most_recent_hash': '0', 'hash_requirement': '0000'}

new block's nonce: 70167, type <class 'int'>
new block's hash: 0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038
new block's hash computed again: 0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038
this blockchain's hash requirement: 0000
new block's current hash: 0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038
new block's prev hash: 0
this blockchain's most recent hash: 0

current chain:
[<block.Block object at 0x7f0314cc5eb0>, <block.Block object at 0x7f0314cd1fd0>]
{'block_number': 1,
 'curr_hash': None,
 'data': 'Genesis',
 'nonce': None,
 'prev_hash': '0',
 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 17, 656148)}
{'block_number': 2,
 'curr_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038',
 'data': 'block 1 data from 10.128.0.7',
 'nonce': 70167,
 'prev_hash': '0',
 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 25, 895599)}
most recent hash: 0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038

Client connected from: ('10.128.0.8', 55902)
chain received: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': '2024-05-07T19:35:34.080435'}], 'block_number': 1, 'most_recent_hash': '0', 'hash_requirement': '0000'}

send channel connected from: 10.128.0.8
dict data sent: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 17, 656148)}, {'block_number': 2, 'data': 'block 1 data from 10.128.0.7', 'prev_hash': '0', 'curr_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038', 'nonce': 70167, 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 25, 895599)}], 'block_number': 2, 'most_recent_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038', 'hash_requirement': '0000'}

current chain:
[<block.Block object at 0x7f0314cc5eb0>, <block.Block object at 0x7f0314cd1fd0>]
{'block_number': 1,
 'curr_hash': None,
 'data': 'Genesis',
 'nonce': None,
 'prev_hash': '0',
 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 17, 656148)}
{'block_number': 2,
 'curr_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038',
 'data': 'block 1 data from 10.128.0.7',
 'nonce': 70167,
 'prev_hash': '0',
 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 25, 895599)}
most recent hash: 0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038
```

Peer 2

```
Internal IP: 10.128.0.7
Expected behavior: send to/receive chain from 10.128.0.6, add new block to its chain, send block to 10.128.0.6 and send chain to 10.128.0.8 (new node)
=====================================================================================================
Client connected from: ('10.128.0.6', 46764)
size of chain data to send: 252
dict data sent: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 25, 737931)}], 'block_number': 1, 'most_recent_hash': '0', 'hash_requirement': '0000'}
chain received: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': '2024-05-07T19:35:17.656148'}], 'block_number': 1, 'most_recent_hash': '0', 'hash_requirement': '0000'}

current chain:
[<block.Block object at 0x7feaa5d01eb0>]
{'block_number': 1,
 'curr_hash': None,
 'data': 'Genesis',
 'nonce': None,
 'prev_hash': '0',
 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 25, 737931)}
most recent hash: 0

block added to 10.128.0.7 per request:
{'block_number': 1,
 'curr_hash': None,
 'data': 'Genesis',
 'nonce': None,
 'prev_hash': '0',
 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 25, 737931)}
{'block_number': 2,
 'curr_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038',
 'data': 'block 1 data from 10.128.0.7',
 'nonce': 70167,
 'prev_hash': '0',
 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 25, 742359)}
sending new block from 10.128.0.7 to <socket.socket fd=6, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('10.128.0.7', 59256), raddr=('10.128.0.6', 55555)>

Client connected from: ('10.128.0.8', 42700)
send channel connected from: 10.128.0.8
size of chain data to send: 534
dict data sent: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 25, 737931)}, {'block_number': 2, 'data': 'block 1 data from 10.128.0.7', 'prev_hash': '0', 'curr_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038', 'nonce': 70167, 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 25, 742359)}], 'block_number': 2, 'most_recent_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038', 'hash_requirement': '0000'}
chain received: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': '2024-05-07T19:35:34.080435'}], 'block_number': 1, 'most_recent_hash': '0', 'hash_requirement': '0000'}

current chain:
[<block.Block object at 0x7feaa5d01eb0>, <block.Block object at 0x7feaa5d252b0>]
{'block_number': 1,
 'curr_hash': None,
 'data': 'Genesis',
 'nonce': None,
 'prev_hash': '0',
 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 25, 737931)}
{'block_number': 2,
 'curr_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038',
 'data': 'block 1 data from 10.128.0.7',
 'nonce': 70167,
 'prev_hash': '0',
 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 25, 742359)}
most recent hash: 0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038
```

Peer 3

```
Internal IP: 10.128.0.8
Expected behavior: send/receive chain from peers 1 and 2
=====================================================================================================
send channel connected from: 10.128.0.6
dict data sent: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 34, 80435)}], 'block_number': 1, 'most_recent_hash': '0', 'hash_requirement': '0000'}

send channel connected from: 10.128.0.7
dict data sent: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 34, 80435)}], 'block_number': 1, 'most_recent_hash': '0', 'hash_requirement': '0000'}

Client connected from: ('10.128.0.7', 36746)
Client connected from: ('10.128.0.6', 57666)

chain received: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': '2024-05-07T19:35:25.737931'}, {'block_number': 2, 'data': 'block 1 data from 10.128.0.7', 'prev_hash': '0', 'curr_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038', 'nonce': 70167, 'timestamp': '2024-05-07T19:35:25.742359'}], 'block_number': 2, 'most_recent_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038', 'hash_requirement': '0000'}

current chain:
[<block.Block object at 0x7fee8a8698e0>, <block.Block object at 0x7fee8a869940>]
{'block_number': 1,
 'curr_hash': None,
 'data': 'Genesis',
 'nonce': None,
 'prev_hash': '0',
 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 34, 145592)}
{'block_number': 2,
 'curr_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038',
 'data': 'block 1 data from 10.128.0.7',
 'nonce': 70167,
 'prev_hash': '0',
 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 34, 145603)}
most recent hash: 0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038

 chain received: {'chain': [{'block_number': 1, 'data': 'Genesis', 'prev_hash': '0', 'curr_hash': None, 'nonce': None, 'timestamp': '2024-05-07T19:35:17.656148'}, {'block_number': 2, 'data': 'block 1 data from 10.128.0.7', 'prev_hash': '0', 'curr_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038', 'nonce': 70167, 'timestamp': '2024-05-07T19:35:25.895599'}], 'block_number': 2, 'most_recent_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038', 'hash_requirement': '0000'}

 current chain:
[<block.Block object at 0x7fee8a8698e0>, <block.Block object at 0x7fee8a869940>]
{'block_number': 1,
 'curr_hash': None,
 'data': 'Genesis',
 'nonce': None,
 'prev_hash': '0',
 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 34, 145592)}
{'block_number': 2,
 'curr_hash': '0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038',
 'data': 'block 1 data from 10.128.0.7',
 'nonce': 70167,
 'prev_hash': '0',
 'timestamp': datetime.datetime(2024, 5, 7, 19, 35, 34, 145603)}
most recent hash: 0000f05398119156ee148923f7103c93a693005e9f08bb20e3bd9fd966f1b038
```

#### Explanation
1. Peers are able to send its chain to each other and update its chain with the longest chain
2. Peers are able to add new blocks to chain per request received from queue
3. Peers are able to send and receive new blocks and update its chain with it