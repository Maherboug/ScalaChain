from cassandra.cluster import Cluster

# Connect to Cassandra
cluster = Cluster(['172.21.0.1', '172.18.0.1', '172.20.0.1', '172.17.0.1'])  # Replace with your Cassandra nodes 
session = cluster.connect()

# Execute CREATE KEYSPACE query
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS offchain
    WITH REPLICATION = {
        'class': 'NetworkTopologyStrategy',
        'DC1': 2  # Adjust based on your datacenter configuration
    }
""")

# Switch to the offchain keyspace
session.set_keyspace('offchain')

# Execute CREATE TABLE query for offchain_ledger
session.execute("""
    CREATE TABLE IF NOT EXISTS offchain_ledger (
        blockindex int,
        transaction_id int,
        sender_address text,
        receiver_address text,
        contract_address text,
        timestamp timestamp,
        value float,
        merkleroot text,
        PRIMARY KEY (blockindex, transaction_id)
    )
""")

# Example: Insert a sample row into offchain_ledger
session.execute("""
    INSERT INTO offchain_ledger (
        blockindex, transaction_id, sender_address, receiver_address,
        contract_address, timestamp, value, merkleroot
    ) VALUES (
        1, 1, '0x123', '0x456', '0x789', '2024-07-25 00:00:00', 123.45, 'root_hash'
    )
""")

# Retrieve schema information for the offchain_ledger table
result = session.execute("""
    SELECT * FROM system_schema.tables
    WHERE keyspace_name = 'offchain' AND table_name = 'offchain_ledger'
""")

# Extract and print schema information
for row in result:
    print("Table:", row.table_name)
    print("Primary Key Columns:", row.primary_key_columns)
    
# Execute SELECT query
rows = session.execute("SELECT * FROM offchain_ledger")
for row in rows:
    print(row.blockindex, row.transaction_id, row.sender_address, row.receiver_address,
          row.contract_address, row.timestamp, row.value, row.merkleroot)

# Query system tables to check replication status
rows = session.execute("SELECT peer, rpc_address, schema_version FROM system.peers")

# Display replication status
for row in rows:
    print("Node:", row.peer)
    print("RPC Address:", row.rpc_address)
    print("Schema Version:", row.schema_version)
    print()

# Close connection
session.shutdown()
cluster.shutdown()
