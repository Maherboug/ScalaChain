# ScalaChain: A Scalable Blockchain Framework with Enhanced Storage and Querying

## Overview

 **ScalaChain** is a Layer 2 solution designed to address the limitations of traditional blockchain systems in storage scalability and data querying. It decouples storage services from blockchain nodes, enabling efficient, secure, and decentralized data management. By combining on-chain and off-chain storage strategies, ScalaChain optimizes storage while maintaining the integrity and accessibility of blockchain data.



## Key Features
- **Storage Optimization:** Reduces on-chain storage by up to 87.2%.  
- **Efficient Querying:** Leverages an indexing mechanism for rapid data retrieval.  
- **Light Node Participation:** Allows resource-constrained devices to participate in the network using a lightweight ledger.  
- **Scalability:** Supports modular storage node architecture for network expansion.  
- **Rapid Synchronization:** Syncs lightweight ledgers 75x faster than traditional blockchain systems.  

## Requirements


- **Python**
- **Flask**
- **Docker & Docker Compose**
- **IPFS**

## Components

### 1. Blockchain Test Node

- **Purpose:** A blockchain test node developed using Python that implements basic functionalities such as block creation, timestamped transaction chaining, consensus, distributed ledger, and peer-to-peer (P2P) network communication.
- **Implementation:** The `BlockchainPy.py` script allows running an instance of this test node on a Flask server.
- **Interaction:**
  - **Send a Transaction:**
    ```bash
    curl -X POST -d "data" http://localhost:5000/transaction
    ```
  - **Read Data:**
    ```bash
    curl -X GET http://localhost:5000/read_request
    ```
  - **Verify Ledger Validity:**
    ```bash
    curl -X GET http://localhost:5000/validate_ledger
    ```

### 2. Gossip Protocol

- **Purpose:** The Epidemic Gossip Protocol is used for peer-to-peer data exchange.
- **Usage:** To run the protocol, execute the `gossip.py` script on each node. Each node will update its local copy of the ledger with new blocks sent by the test node and disseminate the information to neighboring nodes.

### 3. Apache Cassandra

- **Purpose:** A cluster of three Cassandra nodes is used for the off-chain part of the BSaaS approach.
- **Setup:**
  - **Connect to Cassandra:** Use `connectcassandra.py` to create and configure the off-chain environment by setting up keyspaces, tables, replication, and other parameters.
  - **Store Off-Chain Data:** Use `StoreOffchain.py` to store off-chain data from newly received blocks.

### 4. IPFS

- **Purpose:** The InterPlanetary File System (IPFS) is set up as an alternative approach for comparison with our solution.
- **Usage:** You can either run a cluster composed of four nodes or use the Pinata IPFS API service online. Set the necessary tokens and credentials for the Pinata service.


## Indexer API

The **Indexer API** facilitates the indexing of off-chain transactions before storing them in Cassandra nodes. It runs on Flask and provides the following functionalities:

- **Index New Block:** Indexes a new block using a POST request.
  ```bash
  curl -X POST -d "newblock" http://localhost:5001/post_transaction
  ```

- **Read Indexed Data:** Retrieves indexed transaction data using a GET request.
 
  ```bash
    curl -X GET http://localhost:5001/get_transaction
  ```


# Installation and Deployment

## Step 1: Clone the Repository
```bash
git clone https://github.com/your-repo/scalachain.git
cd scalachain
```
## Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```
## Step 3: Set Up Docker Containers
**Start the Cassandra Cluster**
```bash
docker-compose up -d cassandra
```
**Optionally, Set Up IPFS Nodes:**
```bash
docker-compose up -d ipfs
```
**Step 4: Run the Test Node**
```bash
python BlockchainPy.py

```
**Step 5: Start the Indexer API**
```bash
python indexerAPI.py

```

## License

## References
For a detailed overview of the project, watch our introduction video on YouTube: https://youtu.be/MBrqmBnGelI

## Acknowledgments

Thank you for considering contributing to Scalachain! Together, we can build a scalable and efficient blockchain storage solution.