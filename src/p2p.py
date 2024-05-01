from blockchain import Blockchain
from block import Block
from socket import *
import sys
import threading
import time

"""
inspired by bitorrent p2p architecture

new node:
- new node signals tracker by sending its ip address
- new node creates TCP connections with node information received from tracker node
- 

peer nodes:
- tracker node keeps a timer for each peer node and each node periodically notifies tracker of its membership
- maintains blockchain and send/receive blocks over TCP
- two threads for receive() and send() -- is both a server and a client

tracker node:
- default behavior: keeps a timer for each peer node
- when new node joins: records ip addresses of new nodes and randomly sends subset of ip addresses of registered nodes
- when a node leaves: timer runs out and knows the node exited -- remove address from the list

"""

class PeerNetwork:
    def __init__(self, is_tracker: bool, tracker_addr: str, tracker_port: int) -> None:
        self.peers = []
        self.peer_sockets = []
        self.recv_sockets = []
        self.send_sockets = []
        self.tracker_addr = tracker_addr
        self.port = tracker_port
        self.hostname = gethostname()
        self.ip = gethostbyname(self.hostname)
        print("Internal IP:", self.ip)
        self.socket = None
        self.servSock = None
        self.blockchain = Blockchain()
        self.dict = {}  # maps ip to tracker socket connection
        if is_tracker:
            self._handleTracker()
        else:
            self._handleNode()

    def _handleNode(self):
        # add thread for validation of network
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.tracker_addr, self.port))  # connect to tracker node  

        self.servSock = socket(AF_INET, SOCK_STREAM)
        self.servSock.bind((self.ip, self.port))  
        self.servSock.listen()    

        threading.Thread(target=self._nodeTrackerComm, args=()).start()

        while True:
            # Accept client connection and add to list of peers
            client_socket, client_address = self.servSock.accept()
            self.recv_sockets.append(client_socket)
            print(f"Client connected from: {client_address}")

            threading.Thread(target=self._peerComm, args=(client_socket,)).start()  # create a thread for each peer connection (recv channel)
    
    def _peerComm(self, client_socket):
        while True:
            new_block = client_socket.recv(1024).decode()  # receive data from peer
            if not isinstance(new_block, Block):
                continue
            new_block_hash = new_block.mine('0000')
            try:
                # add incoming block to this blockchain
                self.blockchain.add_block(new_block, new_block_hash)
            except Exception as e:
                print(e)
            print("added a block: \n")
            self.blockchain.get_last_block().print_block()

    def _nodeTrackerComm(self):
        while True:
            decoded_data = self.socket.recv(1024).decode()  # receive data from tracker
            # handle query from tracker
            if decoded_data == "OK":  
                self.socket.sendall(self.ip.encode())  # send ip address
            # save updated list of peers from tracker
            else:  
                new_peers = decoded_data.split(",")
                for peer in new_peers:
                    if not peer in self.peers:
                        s = socket(AF_INET, SOCK_STREAM)
                        s.connect((peer, self.port)) 
                        self.peer_sockets.append(s)
                print(f"updated list of peers: {self.peers}\n")
    
    def _send(self, block):
        for sock in self.peer_sockets:
            sock.sendall(block.encode())  # send given data to peers  

    def _handleTracker(self):
        if self.tracker_addr != self.ip:
            raise Exception(f"Invalid tracker address: rerun with {self.ip}\n")
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.tracker_addr, self.port))
        self.socket.listen()

        print(f"Server listening on port: {self.port}\n")

        threading.Thread(target=self._trackerNodeComm, args=()).start()

        while True:
            # Accept client connection and add to list of peers
            client_socket, client_address = self.socket.accept()
            self.peer_sockets.append(client_socket)
            print(f"Client connected from: {client_address}\n")
            print(f"updated list of peers: {self.peer_sockets}\n")
        
    def _trackerNodeComm(self):
        """
        ensures client (each peer) is active in the network

        if client is new, add its ip addres to list of peers and broadcast to others
        if client has left the network (timeout detected), remove its ip address from the list and broadcast to others
        """
        while True:
            for socket in self.peer_sockets:
                socket.sendall("OK".encode())
                socket.settimeout(5)  # set time for client to respond to tracker's query
                try:
                    decoded_data = socket.recv(1024).decode()
                    if not (decoded_data in self.peers):  # client is new
                        self.peers.append(decoded_data)
                        self.dict[socket] = decoded_data
                        print(f"new peer joined: {decoded_data}\n")
                        socket.sendall(",".join(self.peers).encode())  # send updated list of peers
                except socket.timeout:  # client has left
                    self.peer_sockets.remove(socket)
                    self.peers.remove(self.dict[socket])
                    print(f"peer left: {self.dict[socket]}\n")
                    socket.sendall(",".join(self.peers).encode())  # send updated list of peers
        

if __name__ == "__main__":
    tracker_port = int(sys.argv[1]) # the port used to send messages to neighbors
    tracker_addr = sys.argv[2]
    is_tracker = bool(int(sys.argv[3])) # the port used to send messages to neighbors

    p2p_net = PeerNetwork(is_tracker, tracker_addr, tracker_port)
    if not is_tracker:
        last_block = p2p_net.blockchain.get_last_block()
        last_block.print_block()
        new_block = Block(last_block.block_number + 1, 'block 1 data', last_block.prev_hash)
        p2p_net._send(new_block)


