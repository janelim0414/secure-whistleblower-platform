from blockchain import Blockchain
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
    def __init__(self, is_tracker: bool, tracker_port: int) -> None:
        self.peers = []
        self.peer_sockets = []
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
        self.socket.connect(("127.0.0.1", self.port))  # connect to tracker node  

        self.servSock = socket(AF_INET, SOCK_STREAM)
        self.servSock.bind((self.ip, self.port))  
        self.servSock.listen()    

        threading.Thread(target=self._nodeTrackerComm, args=()).start()

        while True:
            new_block = self.servSock.recv(1024).decode()  # receive data from peer
            new_block_hash = new_block.mine('0000')
            try:
                # This is how a block can be added to a blockchain
                self.blockchain.add_block(new_block, new_block_hash)
            except Exception as e:
                print(e)

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
                        socket = socket(AF_INET, SOCK_STREAM)
                        socket.connect((peer, self.port)) 
                        self.peer_sockets.append(socket)
                print(f"updated list of peers: {self.peers}\n")
    
    def _send(self, block):
        for sock in self.peer_sockets:
            sock.sendall(block.encode())  # send given data to peers  

    def _handleTracker(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(("127.0.0.1", self.port))
        self.socket.listen()

        print(f"Server listening on port: {self.port}\n")

        threading.Thread(target=self._trackerNodeComm, args=()).start()

        while True:
            # Accept client connection and add to list of peers
            client_socket, client_address = self.socket.accept()
            self.peer_sockets.append(client_socket)
            print(f"Client connected from: {client_address}")
        
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
                    print(decoded_data)
                    if not decoded_data in self.peers:  # client is new
                        self.peers.append(decoded_data)
                        self.dict[socket] = decoded_data
                        socket.sendall(",".join(self.peers).encode())  # send updated list of peers
                except socket.timeout:  # client has left
                    self.peer_sockets.remove(socket)
                    self.peers.remove(self.dict[socket])
                    socket.sendall(",".join(self.peers).encode())  # send updated list of peers
        

if __name__ == "__main__":
    tracker_port = int(sys.argv[1]) # the port used to send messages to neighbors
    is_tracker = bool(int(sys.argv[2])) # the port used to send messages to neighbors

    PeerNetwork(is_tracker, tracker_port)


