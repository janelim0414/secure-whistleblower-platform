from blockchain import Blockchain
from block import Block
from socket import *
import sys
import threading
import json
import queue

"""
inspired by bitorrent p2p architecture

new node:
- new node signals tracker by sending its ip address
- new node creates TCP connections with node information received from tracker node
- 

peer nodes:
- each peer node periodically notifies tracker of its membership
- maintains blockchain and send/receive blocks over TCP
- two threads for receive() and send() -- is both a server and a client

tracker node:
- default behavior: keeps a timer for each peer node
- when new node joins: records ip addresses of new nodes and randomly sends subset of ip addresses of registered nodes
- when a node leaves: timer runs out and knows the node exited -- remove address from the list

"""

class MsgQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def put_msg(self, block):
        self.queue.put(block)

    def get_msg(self):
        return self.queue.get()
    
    def queue_empty(self):
        return self.queue.empty()

class PeerNetwork:
    def __init__(self, is_tracker: bool, tracker_addr: str, tracker_port: int, msg_q: str) -> None:
        self.peers = []
        self.peer_sockets = []
        self.recv_sockets = []
        self.tracker_addr = tracker_addr
        self.port = tracker_port
        self.hostname = gethostname()
        self.ip = gethostbyname(self.hostname)
        print("Internal IP:", self.ip)
        self.socket = None
        self.servSock = None
        self.msg_q = msg_q
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

            threading.Thread(target=self._receive, args=(client_socket,)).start()  # create a thread for each peer connection (recv channel)
              # create a thread for each peer connection (recv channel)

    def _receive(self, client_socket):
        """
        receive data from each peer/client connection
        """
        while True:
            new_block = client_socket.recv(1024).decode()  # receive data from peer
            if new_block == "":  # peer has disconnected
                client_socket.close()
                self.recv_sockets.remove(client_socket)
                print(f"Client disconnected: {client_socket}")
                break
            new_block = json.loads(new_block)
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
                print(new_peers)
                for peer in new_peers:
                    if not peer in self.peers and peer != self.ip:
                        s = socket(AF_INET, SOCK_STREAM)
                        s.connect((peer, self.port)) 
                        self.peer_sockets.append(s)
                        threading.Thread(target=self._send, args=(s,)).start()
                new_peers.remove(self.ip)
                self.peers = new_peers
                print(f"updated list of peers: {self.peers}\n")
    
    def _send(self, send_sock):
        """
        send to each peer/server connection
        """
        while True:
            if not self.msg_q.queue_empty():
                msg = self.msg_q.get_msg()  # retreive message from queue
                last_block = self.blockchain.get_last_block()
                last_block.print_block()
                new_block = Block(last_block.block_number + 1, msg, last_block.prev_hash)  # create block from message
                block_to_send = json.dumps(new_block)
                print(f"sending new block from {self.ip} to {send_sock}")
                send_sock.sendall(block_to_send.encode())  # send given data to peers  

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
                    print(self.peer_sockets)
                    print(self.peers)
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
                print(f"Updated list of peers sent to {s}: {self.peers}")

    def _handleNewPeer(self, socket, peer_ip):
        """
        Handle the scenario where a new peer joins the network.
        """
        self.peers.append(peer_ip)
        self.dict[socket] = peer_ip
        print(f"New peer joined: {peer_ip}\n")
        for s in self.peer_sockets:
            s.sendall(",".join(self.peers).encode())  # Send updated list of peers
            print(f"Updated list of peers sent to {s}: {self.peers}")
        

if __name__ == "__main__":
    tracker_port = int(sys.argv[1]) # the port used to send messages to neighbors
    tracker_addr = sys.argv[2]
    is_tracker = bool(int(sys.argv[3])) # the port used to send messages to neighbors

    def run_p2p_net(msg_q):
        PeerNetwork(is_tracker, tracker_addr, tracker_port, msg_q)

    # Start the PeerNetwork class in a separate thread
    msg_q = MsgQueue()
    peer_network_thread = threading.Thread(target=run_p2p_net, args=(msg_q,))
    peer_network_thread.start()

    print("here")
    if not is_tracker:
        msg_q.put_msg('block 1 data')


