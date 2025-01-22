from flask import Flask, request, jsonify
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import json

app = Flask(__name__)

# Cassandra connection setup
def get_cassandra_session():
    cluster = Cluster(['127.0.0.1'])  # Replace with your Cassandra contact points
    session = cluster.connect('offchain')  # Connect to the 'offchain' keyspace
    return session

# Insert transaction into Cassandra
def insert_transaction(transaction_id, sender_address, receiver_address, timestamp, value):
    session = get_cassandra_session()
    insert_statement = SimpleStatement("""
        INSERT INTO ledger_offchain (transaction_id, sender_address, receiver_address, timestamp, value)
        VALUES (%s, %s, %s, %s, %s)
    """)
    session.execute(insert_statement, (transaction_id, sender_address, receiver_address, timestamp, value))

@app.route('/post_transaction', methods=['POST'])
def post_transaction():
    try:
        # Parse the posted JSON data
        data = request.get_json()
        transaction_id = data['transaction_id']
        sender_address = data['sender_address']
        receiver_address = data['receiver_address']
        timestamp = data['timestamp']
        value = data['value']
        
        # Insert transaction into Cassandra
        insert_transaction(transaction_id, sender_address, receiver_address, timestamp, value)
        
        return jsonify({'message': 'Transaction inserted successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/get_transaction', methods=['GET'])
def get_transaction():
    try:
        # Read query parameters
        transaction_id = request.args.get('transaction_id')
        sender_address = request.args.get('sender_address')
        receiver_address = request.args.get('receiver_address')
        timestamp = request.args.get('timestamp')
        value = request.args.get('value')

        # Prepare the query
        session = get_cassandra_session()
        query = "SELECT * FROM ledger_offchain WHERE "
        conditions = []
        params = []

        if transaction_id:
            conditions.append("transaction_id = %s")
            params.append(transaction_id)
        if sender_address:
            conditions.append("sender_address = %s")
            params.append(sender_address)
        if receiver_address:
            conditions.append("receiver_address = %s")
            params.append(receiver_address)
        if timestamp:
            conditions.append("timestamp = %s")
            params.append(timestamp)
        if value:
            conditions.append("value = %s")
            params.append(value)

        query += " AND ".join(conditions)

        # Execute the query
        statement = SimpleStatement(query)
        rows = session.execute(statement, params)
        
        # Format the results
        results = [dict(row) for row in rows]

        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)

