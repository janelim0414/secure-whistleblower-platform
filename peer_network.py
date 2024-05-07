import socket
import sys
import threading

class PeerNetwork:
    def __init__(self, is_tracker: bool, tracker_port: int) -> None:
        self.peers = []
        self.peer_sockets = []
        self.port = tracker_port
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        print("Internal IP:", self.ip)
        self.socket = None
        if is_tracker:
            self._handleTracker()
        else:
            self._handleNode()

    def _handleNode(self):
        # add thread for validation of network
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("127.0.0.1", self.port))        
        self.socket.sendall(self.ip.encode())
        print("Sent", len(self.ip.encode()), "bytes")
        decoded_data = self.socket.recv(1024).decode()
        print(decoded_data)


    def _handleTracker(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("127.0.0.1", self.port))
        self.socket.listen()

        print(f"Server listening on port: {self.port}")

        threading.Thread(target=self._validateNetwork, args=()).start()

        while True:
            # Accept client connection
            client_socket, client_address = self.socket.accept()
            self.peer_sockets.append(client_socket)
            print(f"Client connected from: {client_address}")

            # Start thread to handle client
            threading.Thread(target=self._handleNodeComm, args=(client_socket,)).start()
        
    def _validateNetwork(self):
        # Execute this based on timer timeout
        for socket in self.peer_sockets:
            socket.sendall("OK".encode())
            if socket.recv(1024).decode() != "OK":
                self.peer_sockets.remove(socket)

    def _handleNodeComm(self, client: socket):
        decoded_data = client.recv(1024).decode()
        print(decoded_data)
        if not decoded_data in self.peers:
            self.peers.append(decoded_data)
        client.sendall(",".join(self.peers).encode())

if __name__ == "__main__":
    tracker_port = int(sys.argv[1]) # the port used to send messages to neighbors
    is_tracker = bool(int(sys.argv[2])) # the port used to send messages to neighbors

    PeerNetwork(is_tracker, tracker_port)