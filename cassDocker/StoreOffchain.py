import json
import re
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# Cassandra connection setup
cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra contact points
session = cluster.connect('offchain')  # Connect to the 'offchain' keyspace

# Create a statement for inserting data
insert_statement = SimpleStatement("""
    INSERT INTO ledger_offchain (blockindex, transaction_id, sender_address, receiver_address, contract_address, timestamp, value, merkleroot)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

# Function to parse transaction details from the string
def parse_transactions(tx_string):
    tx_string_cleaned = tx_string.replace("'", "")
    transactions = re.findall(r'from_address:\s*(\S+),\s*to_address:\s*(\S+),\s*contract_address:\s*(\S+),\s*value:\s*([\d.]+)', tx_string_cleaned)
    return transactions

# Function to process each block from the file
def process_block(block_data):
    # Extract block details
    blockindex = block_data.get("index", 0)
    previous_hash = block_data.get("previous_hash", "")
    timestamp = block_data.get("timestamp", "")
    merkle_root = block_data.get("merkle_root", "")
    hash_value = block_data.get("hash", "")
    transactions = block_data.get("transactions", [])
    
    # Initialize lists
    from_addresses = []
    to_addresses = []
    contract_addresses = []
    values = []

    # Parse transactions
    for tx_string in transactions:
        parsed_transactions = parse_transactions(tx_string)
        for tx in parsed_transactions:
            from_addresses.append(tx[0])
            to_addresses.append(tx[1])
            contract_addresses.append(tx[2])
            values.append(float(tx[3]))

    # Insert data into Cassandra
    for i, (from_address, to_address, contract_address, value) in enumerate(zip(from_addresses, to_addresses, contract_addresses, values)):
        session.execute(insert_statement, (blockindex, i, from_address, to_address, contract_address, timestamp, value, merkle_root))

# Read and process the JSON file
with open('ledg.json', 'r') as file:
    for line in file:
        try:
            block_data = json.loads(line.strip())
            process_block(block_data)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Close Cassandra connection
cluster.shutdown()
