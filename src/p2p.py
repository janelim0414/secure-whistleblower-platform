from blockchain import Blockchain
from block import Block
from socket import *
import sys
import threading
import json
import queue
from datetime import datetime
import copy

"""
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
"""
def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
        
class MsgQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def put_msg(self, msg, dst):
        """
        given a message and a destination ip address (peer),
        create a tuple and push it to queue for the specified peer to process (create block and add)
        """
        self.queue.put((msg, dst))

    def get_msg(self):
        return self.queue.get()
    
    def queue_empty(self):
        return self.queue.empty()

class PeerNetwork:
    def __init__(self, is_tracker: bool, tracker_addr: str, tracker_port: int, msg_q: MsgQueue) -> None:
        self.peers = []
        self.peer_sockets = []
        self.recv_sockets = []
        self.tracker_addr = tracker_addr
        self.port = tracker_port
        self.hostname = gethostname()
        self.ip = gethostbyname(self.hostname)
        self.socket = None
        self.servSock = None
        self.msg_q = msg_q
        self.blockchain = Blockchain()
        self.dict = {}  # maps ip to tracker socket connection
        if is_tracker:
            threading.Thread(target=self._handleTracker, args=()).start()
            #self._handleTracker()
        else:
            threading.Thread(target=self._handleNode, args=()).start()
            #self._handleNode()

    def _handleNode(self):
        # add thread for validation of network
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.tracker_addr, self.port))  # connect to tracker node  

        self.servSock = socket(AF_INET, SOCK_STREAM)
        self.servSock.bind((self.ip, self.port))  
        self.servSock.listen()    
        # Start a thread to initiate communication on the node side
        threading.Thread(target=self._nodeTrackerComm, args=()).start()

        while True:
            # Accept client connection and add to list of peers
            client_socket, client_address = self.servSock.accept()
            self.recv_sockets.append(client_socket)
            print(f"Client connected from: {client_address}")
            # Create a thread for each peer connection (recv channel)
            threading.Thread(target=self._receive, args=(client_socket,)).start()  

    def _receive(self, client_socket):
        """
        receive data from each peer/client connection
        """
        while True:
            header = client_socket.recv(1).decode()  # receive data from peer
            if header == "":  # peer has disconnected
                client_socket.close()
                self.recv_sockets.remove(client_socket)
                print(f"Client disconnected: {client_socket}")
                break
            elif header == "c":  # chain received from peers
                chain_data = client_socket.recv(1024).decode() 
                chain_data = json.loads(chain_data)
                chain = Blockchain(**chain_data)
                blocks = []
                for block_data in chain_data["chain"]:
                    block = Block(**block_data)
                    blocks.append(block)
                chain.chain = blocks
                print(f"Chain received: {chain.print_chain()}")
                if len(chain.chain) > len(self.blockchain.chain):
                    self.blockchain = chain  # update chain with longest 
                    print(f"Chain updated: {self.blockchain.print_chain()}")
            elif header == "b":  # new block added by other peer
                new_block = client_socket.recv(1024).decode() 
                new_block = json.loads(new_block)
                new_block = Block(**new_block)
                try:
                    # add incoming block to this blockchain
                    self.blockchain.add_block(new_block, new_block.curr_hash)
                    print(f"Block added: {self.blockchain.print_chain()}")
                except Exception as e:
                    print(e)

    def _nodeTrackerComm(self):
        """
        communicate with tracker to update list of peers across network
        handle newly joined peers by sending this node's blockchain
        """
        while True:
            decoded_data = self.socket.recv(1024).decode()  # receive data from tracker
            # handle query from tracker
            if decoded_data == "OK":  
                self.socket.sendall(self.ip.encode())  # send ip address
            # save updated list of peers from tracker
            else:  
                new_peers = decoded_data.split(",")
                for peer in new_peers:
                    if (not peer in self.peers) and (peer != self.ip):
                        # create send channel from this node to newly joined node
                        s = socket(AF_INET, SOCK_STREAM)
                        s.connect((peer, self.port)) 
                        self.peer_sockets.append(s)
                        # send chain of this node to newly joined node
                        chain_copy = copy.deepcopy(self.blockchain)
                        for i in range(len(chain_copy.chain)):
                            block = chain_copy.chain[i]
                            chain_copy.chain[i] = block.__dict__
                        chain_data = json.dumps(chain_copy.__dict__, default=datetime_serializer)
                        header = "c".encode()  # "c" for chain
                        s.sendall(header + chain_data.encode())
                        # start thread for sending blocks for this peer
                        threading.Thread(target=self._send, args=(s,)).start()
                # update list of peers
                new_peers.remove(self.ip)
                self.peers = new_peers
                print(f"Updated peers: {self.peers}\n")
    
    def _send(self, send_sock):
        """
        send to each peer/server connection
        """
        while True:
            if not self.msg_q.queue_empty():
                #Sending message
                msg = self.msg_q.get_msg()  # retreive put request from queue
                if msg[1] == self.ip:  # if the req is not for this node, skip and wait for more
                    continue
                # add block to this node's chain
                last_block = self.blockchain.get_last_block()
                last_block.print_block()
                block_number = msg[0]['block_number']
                message = msg[0]['data']
                prev_hash = msg[0]['prev_hash']
                #new_block = Block(last_block.block_number + 1, msg[0], last_block.curr_hash)  # create block from message
                new_block = Block(block_number, message, prev_hash)
                new_hash = new_block.mine('0000')  # get hash to verify block
                try:
                    self.blockchain.add_block(new_block, new_hash)  # add to this node's chain as requested
                except Exception as e:
                    print(e)
                print(f"Block added to {self.ip}")
                # send block to peers
                block_to_send = json.dumps(new_block.__dict__, default=datetime_serializer)
                header = "b".encode()  # "b" for block
                print(f"Sending new block from {self.ip} to {send_sock}")
                send_sock.sendall(header + block_to_send.encode())  # send block to peers  

    def _handleTracker(self):
        if self.tracker_addr != self.ip:
            raise Exception(f"Invalid tracker address: rerun with {self.ip}\n")
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.tracker_addr, self.port))
        self.socket.listen()
        print(f"Server listening on port: {self.port}\n")
        # Start a thread to initiate communication on the tracker side
        threading.Thread(target=self._trackerNodeComm, args=()).start()

        while True:
            # Accept client connection and add to list of peers
            client_socket, client_address = self.socket.accept()
            self.peer_sockets.append(client_socket)
            print(f"Client connected from: {client_address}\n")
        
    def _trackerNodeComm(self):
        """
        Ensure each peer is active in the network.

        If a peer is new, add its IP address to the list of peers and broadcast to others.
        If a peer has left the network (timeout detected), remove its IP address from the list and broadcast to others.
        """
        while True:
            for socket in self.peer_sockets:
                try:
                    socket.sendall("OK".encode())
                    decoded_data = socket.recv(1024).decode()
                    if decoded_data == "":  # Peer has left
                        self._handlePeerLeave(socket)
                    elif decoded_data not in self.peers:  # Peer is new
                        self._handleNewPeer(socket, decoded_data)
                except ConnectionResetError:
                    # Handle the case where the peer disconnects abruptly
                    self._handlePeerLeave(socket)

    def _handlePeerLeave(self, socket):
        """
        Handle the scenario where a peer leaves the network.
        """
        peer_ip = self.dict.pop(socket, None)
        if peer_ip:
            print(f"Peer left: {peer_ip}\n")
            socket.close()  # Close the socket
            self.peer_sockets.remove(socket)
            self.peers.remove(peer_ip)
            for s in self.peer_sockets:
                s.sendall(",".join(self.peers).encode())  # Send updated list of peers

    def _handleNewPeer(self, socket, peer_ip):
        """
        Handle the scenario where a new peer joins the network.
        """
        self.peers.append(peer_ip)
        self.dict[socket] = peer_ip
        print(f"New peer joined: {peer_ip}\n")
        for s in self.peer_sockets:
            s.sendall(",".join(self.peers).encode())  # Send updated list of peers
        

if __name__ == "__main__":
    tracker_port = int(sys.argv[1])
    tracker_addr = sys.argv[2]
    is_tracker = bool(int(sys.argv[3]))

    def run_p2p_net(msg_q):
        PeerNetwork(is_tracker, tracker_addr, tracker_port, msg_q)

    # Start the PeerNetwork class in a separate thread
    msg_q = MsgQueue()
    peer_network_thread = threading.Thread(target=run_p2p_net, args=(msg_q,))
    peer_network_thread.start()


