import requests

# API credentials
api_key = 'f6c0026bd80003351194'
api_secret = 'b46bd9d2ff3370cba5f01be8b128e580a77d737422a028765f2d3cf5d263097e'

# URL to get pinned files from Pinata
url = "https://api.pinata.cloud/data/pinList"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Function to retrieve the pinned file
def retrieve_pinned_files():
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Return the response in JSON format
    else:
        return {"error": f"Request failed with status code {response.status_code}"}

# Call the function and print the results
file_data = retrieve_pinned_files()
print("Retrieved Data:", file_data)
