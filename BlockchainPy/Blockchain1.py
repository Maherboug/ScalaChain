import hashlib
import time
from datetime import datetime
import json
from flask import Flask, request
from merklelib import MerkleTree

# Define the block structure
class Block:
    def __init__(self, index, previous_hash, timestamp, merkle_root, hash, nonce, transactions):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.merkle_root = merkle_root
        self.hash = hash
        self.nonce = nonce
        self.transactions = transactions

    def calculate_hash(self):
        block_data = str(self.index) + str(self.previous_hash) + str(self.timestamp)  + str(self.merkle_root) + str(self.nonce) + str(self.transactions)
        return hashlib.sha256(block_data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = self.read_from_file()  # Initialize chain from file
        if not self.chain:  # If no ledger exists or is empty, create a new one with a genesis block
            self.chain = [self.create_genesis_block()]
            self.write_to_file(self.chain[0])  # Write the genesis block to the ledger file
        self.index = len(self.chain)  # Set index to the length of the chain
    def create_genesis_block(self):
       return Block(0, "0", str(datetime.now()), "", hashlib.sha256("0".encode()).hexdigest(), 0, [])
   
    # # This is the function for proof of work
    # and used to successfully mine the block
    def create_new_block(self, previous_block, transactions, difficulty):
        index = previous_block.index + 1
        timestamp = str(datetime.now())
        nonce = 0
        # Calculate the Merkle root for the transactions
        merkle_tree = MerkleTree(transactions)
        merkle_root = merkle_tree.merkle_root 
        while True:
            hash_attempt = Block(index, previous_block.hash, timestamp, merkle_root, "", nonce, transactions).calculate_hash()
            if hash_attempt.startswith("0" * difficulty):
                break
            nonce += 1

        return Block(index, previous_block.hash, timestamp, merkle_root, hash_attempt, nonce, transactions)
    def search_ledger(self, query_transaction, query_timestamp):
        for block in self.chain:
            for transaction in block.transactions:
                if query_transaction in transaction and block.timestamp == query_timestamp:
                    return block
        return None


    def write_to_file(self, data, is_block=True):
        with open('ledger.json', 'a') as ledger_file:
            ledger_file.write(json.dumps(data.__dict__) + '\n')

    def read_from_file(self):
        try:
            with open('ledger.json', 'r') as ledger_file:
                lines = ledger_file.readlines()
                return [Block(**json.loads(line)) for line in lines]
        except FileNotFoundError:
            return []
    def is_valid(self):
        Myledger = self.read_from_file()
        return self.validate_ledge(Myledger)

    def validate_ledge(self, ledger):
        for i in range(1, len(ledger)):
            current_block = ledger[i]
            previous_block = ledger[i - 1]

            if current_block.calculate_hash() != current_block.hash:
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# Initialize the blockchain 
blockchain = Blockchain()
difficulty = 4

app = Flask(__name__)

# API endpoint to send a request to another node
@app.route('/send_request', methods=['POST'])
def send_request():
    data = request.form['data']
      # Check if the ledger is empty or does not exist
    current_block = blockchain.chain[-1]
    print("current_block", current_block)
    current_block.transactions.append(data)

    # Check if the number of transactions in the current block is 5 or more it depend on the blocklimit strategy
    if len(current_block.transactions) >= 1:
        # If the current block is full, create a new block
        new_block = blockchain.create_new_block(current_block, [data], difficulty)
        blockchain.chain.append(new_block)
        blockchain.write_to_file(new_block)

        # Start a new set of transactions for the next block
        current_block.transactions = []

    response = {'message': 'Request sent successfully!'}
    return json.dumps(response), 200

@app.route('/read_request', methods=['POST'])
def read_request():  
    # Get the data from the POST request
    data = request.form['data']
    query_transaction, query_timestamp = data.split(',')  # Assuming data is in the format "transactions,timestamp"
    print(query_transaction)
    # Search the ledger for the specified data
    result = blockchain.search_ledger(query_transaction.strip(), query_timestamp.strip())
    print(result)
    
    if result:
        response = {
            "index": result.index,
            "previous_hash": result.previous_hash,
            "timestamp": result.timestamp,
            "merkle_root": result.merkle_root,
            "hash": result.hash,
            "nonce": result.nonce,
            "transactions": result.transactions
        }
        return json.dumps(response), 200
    else:
        response = {"message": "Data not found in the ledger."}
        return json.dumps(response), 404

# API endpoint to validate the ledger
@app.route('/validate_ledger', methods=['GET'])
def validate_ledger():
    is_valid = blockchain.is_valid()

    if is_valid:
        response = {'message': 'The ledger is valid.'}
    else:
        response = {'message': 'The ledger is not valid.'}

    return json.dumps(response), 200

# API endpoint to get the ledger (chain)
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})
# Run the Flask app
if __name__ == '__main__':
        app.run(port=5000, debug=True)

