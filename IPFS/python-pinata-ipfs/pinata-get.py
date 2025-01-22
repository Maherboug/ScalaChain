import requests
import os
from dotenv import load_dotenv
import json
import pprint

# Load environment variables
load_dotenv()

def upload_to_pinata(jwt_token, ipfs_hash):
    url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    headers = {'Authorization': f'Bearer {jwt_token}'}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.content  # Return the file content
    else:
        return {"error": f"Request failed with status code {response.status_code}"}

# Environment variable for the JWT token
PINATA_JWT_TOKEN = os.getenv('PINATA_JWT_TOKEN')

# Example IPFS hash to retrieve a file
ipfs_hash = 'QmExampleHash'  # Replace with the actual IPFS hash of the file

# Retrieve the file
file_data = upload_to_pinata(PINATA_JWT_TOKEN, ipfs_hash)

# Save the file locally
file_path = 'retrieved_file1.json'
if isinstance(file_data, dict):
    pprint.pprint(file_data)
else:
    with open(file_path, 'wb') as f:
        f.write(file_data)

    # Open and read the JSON file
    with open(file_path, 'r') as f:
        json_data = json.load(f)
    
    # Filter transactions where "index": 5
    transactions = [block['transactions'] for block in json_data if block.get('index') == 15]
    
    # Flatten the list of transactions
    all_transactions = [tx for sublist in transactions for tx in sublist]

    # Print the filtered transactions
    pprint.pprint(all_transactions)
    print(f"Filtered transactions with index 5 from '{file_path}'.")
