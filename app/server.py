from flask import Flask, request, render_template_string, jsonify
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
    <pre id="blockchainDisplay">Loading blockchain...</pre>

    <script>
        function fetchBlockchain() {
            fetch('/get_blockchain')
            .then(response => response.json())
            .then(data => {
                document.getElementById('blockchainDisplay').innerText = data.blockchain;
            })
            .catch(error => console.error('Error fetching blockchain:', error));
        }

        // Poll for new blockchain data every 5 seconds
        setInterval(fetchBlockchain, 5000);

        // Fetch immediately on page load
        fetchBlockchain();
    </script>
    </body>
</html>
"""


@app.route('/get_blockchain')
def get_blockchain():
    """
    Flask Route for receiving and printing blockchain data

    returns: str - representing blockchain data
    """
    blockchain_data = peer_network.blockchain.print_chain()
    print(blockchain_data)
    return jsonify({'blockchain': blockchain_data or "No blocks in the blockchain."})

@app.route('/', methods=['GET'])
def home():
    """
    Flask Route for home page to display html template with blockchain data

    returns: str - representing html template
    """
    blockchain_data = peer_network.blockchain.print_chain()
    if not blockchain_data.strip():
        blockchain_data = "No blocks in the blockchain."
    return render_template_string(HTML_TEMPLATE, blockchain=blockchain_data)

# Flask Route
@app.route('/submit', methods=['POST'])
def submit():
    """
    Flask route for submitting/adding blocks to blockchain
    using message from POST request

    message - text from form field (str) 

    return: str - representing the home page html with new blockchain data
    """
    message = request.form['message']
    if message:
        last_block = peer_network.blockchain.get_last_block()
        #if last_block.block_number == 1:
        #    new_block = Block(last_block.block_number + 1, message, last_block.prev_hash)
        #else:
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
    """
    Initializes global variable peer_network using defined input parameters

    arguments:
    is_tracker - represents if current node is tracker (bool)
    tracker_addr - represents the internal IP address of tracker node (str)
    """
    try:
        global peer_network
        tracker_port = 8000
        peer_network = PeerNetwork(is_tracker, tracker_addr, tracker_port, msg_q)
    except Exception as e:
        print(f"Error running P2P network: {e}")


def find_available_port():
    """
    Helper function to find an available port to avoid socket errors

    returns: (int) representing available port
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


if __name__ == '__main__':
    tracker_addr = sys.argv[1]
    is_tracker = bool(int(sys.argv[2]))
    threading.Thread(target=run_p2p_network, args=(is_tracker, tracker_addr, )).start()
    app.run(debug=False, port=find_available_port())