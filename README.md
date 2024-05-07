[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/-Lgd7v9y)
# CSEE 4119 Spring 2024, Class Project
## Team name: Blockchain Smoker
## Team members (name, GitHub username):
* Jane Lim - janelim0414
* Tattie Chitrakorn - tchitrakorn
* Karen Wang - karenswang
* Charlie Heus - Charlie-Heus

# How to Run Code:

## To Run Code as Tracker: 
`python app/server.py <tracker_internal_ip> 1` 

## To Run Code as Peer:
`python app/server.py <tracker_internal_ip> 0`

# Description of each file: 

## block.py:

This file defines a Python class called Block, which serves as a basic implementation of a block which is concatenated together in a blockchain data structure. The Block class encapsulates functionalities essential for managing a blockchain network, including block creation, validation, and mining. It also has a print_block function that can be used for debugging. 

## blockchain.py:

This file defines a Python class Blockchain which represents a basic implementation of a blockchain data structure containing blocks from the Block class. This class handles the management of all of the blocks. It creates a genesis block which is a dummy node at the start of the blockchain. It also implements a validation system which uses hashes before adding the block to the blockchain protecting against corruption of the chain. 

## blockchain_sandbox.py:

This Python script demonstrates the usage of the Block and Blockchain classes from a blockchain implementation. It simulates interactions between nodes.

Node 1: Initializes a Blockchain object and adds a new block ('block 1 data') to it. Demonstrates the creation and addition of blocks to the blockchain, including mining for a valid hash.

Node 2: Clones the blockchain from Node 1. Attempts to add invalid blocks to its local blockchain to illustrate error handling scenarios, such as providing an invalid previous hash or an invalid current hash.Receives a valid block from Node 1 and successfully adds it to its blockchain. 

This script serves as a sandbox environment to illustrate the behavior of blockchain nodes, including block creation, validation, and addition to the blockchain. It helps understand how nodes interact and maintain consensus within a decentralized network.

## test_blockchain.py:
This is a testing script for all block and blockchain related functionalities. Please see more information in `TESTING.md`.

## p2p.py:

This Python file implements a simplified peer-to-peer (P2P) blockchain network using TCP sockets for communication. The nodes in the network carry out the following functionality: 

new node:
- new node signals tracker by sending its ip address
- new node creates TCP connections with node information received from tracker node
- new node receives longest chain from peers upon joining

peer nodes:
- each peer node periodically notifies tracker of its membership
- maintains blockchain and send/receive blocks over TCP
- two threads for receive() and send() -- is both a server and a client
- each peer sends its chain to new node
- send new block to all peers

tracker node:
- default behavior: keeps a timer for each peer node
- when new node joins: records ip addresses of new nodes and sends ip addresses of registered nodes
- when a node leaves: no response from peer and knows the node exited -- remove address from the list
