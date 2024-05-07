from flask import Flask, request, render_template, jsonify
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

@app.route('/get_blockchain')
def get_blockchain():
    blockchain_data = peer_network.blockchain.print_chain()
    print(blockchain_data)
    return jsonify({'blockchain': blockchain_data or "No blocks in the blockchain."})

@app.route('/', methods=['GET'])
def home():
    blockchain_data = peer_network.blockchain.print_chain()
    if not blockchain_data.strip():
        blockchain_data = "No blocks in the blockchain."
    return render_template('index.html', blockchain=blockchain_data)

@app.route('/submit', methods=['POST'])
def submit():
    message = request.form['message']
    if message:
        last_block = peer_network.blockchain.get_last_block()
        new_block = Block(last_block.block_number + 1, message, last_block.curr_hash)
        new_block_hash = new_block.mine('0000')
        peer_network.blockchain.add_block(new_block, new_block_hash)
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
    threading.Thread(target=run_p2p_network, args=(is_tracker, tracker_addr)).start()
    app.run(debug=False, port=find_available_port())
