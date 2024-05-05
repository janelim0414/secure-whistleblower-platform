from flask import Flask, request, render_template_string, jsonify
from flask_socketio import SocketIO, emit
import sys
import os
import threading
import socket

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from blockchain import Blockchain
from p2p import PeerNetwork, MsgQueue
from block import Block

# Initialize the blockchain and P2P network
blockchain = Blockchain()
msg_q = MsgQueue()
peer_network = None

app = Flask(__name__)
socketio = SocketIO(app)

# HTML template for the home page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Whistleblower App</title>
</head>
<body>
    <h1>Whistleblower Blockchain Application</h1>
    <form action="/submit" method="post">
        <label for="message">Message:</label><br>
        <textarea id="message" name="message" rows="4" cols="50"></textarea><br>
        <input type="submit" value="Submit">
    </form>
    <h2>Blockchain:</h2>
    <pre id="blockchainDisplay">{{ blockchain }}</pre>
</body>
<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.0/socket.io.js"></script>
<script>
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('update_blockchain', function(data) {
    document.getElementById('blockchainDisplay').innerText = data.blockchain;
});
</script>
</html>
"""

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Connected'})

def notify_flask_app_of_update():
    socketio.emit('update_blockchain', {'blockchain': blockchain.print_chain()})

@app.route('/', methods=['GET'])
def home():
    blockchain_data = blockchain.print_chain()
    if not blockchain_data.strip():
        blockchain_data = "No blocks in the blockchain."
    return render_template_string(HTML_TEMPLATE, blockchain=blockchain_data)

@app.route('/submit', methods=['POST'])
def submit():
    message = request.form['message']
    if message:
        last_block = blockchain.get_last_block()
        if last_block.block_number == 1:
            new_block = Block(last_block.block_number + 1, message, last_block.prev_hash)
        else:
            new_block = Block(last_block.block_number + 1, message, last_block.curr_hash)
        new_block_hash = new_block.mine('0000')
        blockchain.add_block(new_block, new_block_hash)
        if peer_network is not None:
            peers = peer_network.peers
            for peer in peers:
                msg_q.put_msg(new_block.to_dict(), peer)      
        return home()
    else:
        return home()

def run_p2p_network(is_tracker, tracker_addr):
    try:
        global peer_network
        tracker_port = 8000
        peer_network = PeerNetwork(is_tracker, tracker_addr, tracker_port, msg_q)
        peer_network_thread = threading.Thread(target=peer_network.run)
        peer_network_thread.start()
    except Exception as e:
        print(f"Error running P2P network: {e}")


def find_available_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


if __name__ == '__main__':
    tracker_addr = sys.argv[1]
    is_tracker = bool(int(sys.argv[2]))
    threading.Thread(target=run_p2p_network, args=(is_tracker, tracker_addr, )).start()
    app.run(debug=True, port=find_available_port())