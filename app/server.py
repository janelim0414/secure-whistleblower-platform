from flask import Flask, request, render_template_string, jsonify
import sys
import os
import threading

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
    <pre id="blockchainDisplay">{{ blockchain }}</pre>
</body>
<script>
function fetchBlockchain() {
    fetch('/')
        .then(response => response.text())
        .then(html => {
            var parser = new DOMParser();
            var doc = parser.parseFromString(html, 'text/html');
            var blockchainData = doc.querySelector('pre').innerText;
            document.getElementById('blockchainDisplay').innerText = blockchainData;
        });
}

setInterval(fetchBlockchain, 1000);  // Update every 1000 milliseconds (1 second)
</script>
</html>
"""

# peers = ['10.128.0.3', '10.128.0.4', '10.128.0.6']

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
        new_block = Block(last_block.block_number + 1, message, last_block.prev_hash)
        new_block_hash = new_block.mine('0000')
        blockchain.add_block(new_block, new_block_hash)
        # Broadcast the new block to peers
        msg_q.put_msg((new_block.to_dict(), '10.128.0.4'))
        msg_q.put_msg((new_block.to_dict(), '10.128.0.6'))
    else:
        return home()

def run_p2p_network():
    try:
        global peer_network
        is_tracker = False  # True for tracker node
        tracker_addr = '10.128.0.5' 
        tracker_port = 8000 
        peer_network = PeerNetwork(is_tracker, tracker_addr, tracker_port, msg_q)
        peer_network_thread = threading.Thread(target=peer_network.run)
        peer_network_thread.start()
    except Exception as e:
        print(f"Error running P2P network: {e}")

if __name__ == '__main__':
    threading.Thread(target=run_p2p_network).start()
    app.run(debug=True)
