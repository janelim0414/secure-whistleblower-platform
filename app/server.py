from flask import Flask, request, render_template_string, jsonify
import sys
import os
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from blockchain import Blockchain
from p2p import PeerNetwork, MsgQueue
from block import Block

# Initialize the blockchain
blockchain = Blockchain()
app = Flask(__name__)

# The basic HTML template for the home page
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

setInterval(fetchBlockchain, 5000);  // Update every 5000 milliseconds (5 seconds)
</script>
</html>
"""
@app.route('/', methods=['GET'])
def home():
    # Display the blockchain
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
        new_block_hash = new_block.mine('0000')  # Assuming a difficulty level of '0000'
        try:
            blockchain.add_block(new_block, new_block_hash)
            response_message = 'New block added successfully!'
        except Exception as e:
            response_message = str(e)
        # return jsonify({'message': response_message, 'hash': new_block_hash if 'added' in response_message else 'N/A'}), 200
        return home()
    else:
        # return jsonify({'error': 'No message provided'}), 400
        return home()

# def run_p2p_network():
#     msg_q = MsgQueue()
#     is_tracker = False
#     tracker_addr = 'localhost'  # Example address
#     tracker_port = 8000  # Example port
#     peer_network = PeerNetwork(is_tracker, tracker_addr, tracker_port, msg_q)
#     peer_network_thread = threading.Thread(target=peer_network.run)
#     peer_network_thread.start()

if __name__ == '__main__':
    # Run P2P network in the background
    # threading.Thread(target=run_p2p_network).start()
    # Start Flask app
    app.run(debug=True)
