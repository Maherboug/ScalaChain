# Pinata IPFS Uploader

Simple script to upload files to IPFS using Pinata.

## Setup

1. **Clone Repository**: 
   - For HTTPS: 
     ```
     git clone https://github.com/codingcouchyt/python-pinata-ipfs-minimal
     ```
   - For SSH: 
     ```
     git clone git@github.com:codingcouchyt/python-pinata-ipfs-minimal.git
     ```

2. **Set Up Virtual Environment**:
   - Navigate to the cloned directory:
     ```
     cd python-pinata-ipfs-minimal
     ```
   - Create a virtual environment:
     ```
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```
       .\venv\Scripts\activate
       ```
     - On Unix or MacOS:
       ```
       source venv/bin/activate
       ```

3. **Install Dependencies**: 
   - With the virtual environment activated, install the required packages:
     ```
     pip install requests python-dotenv
     ```

4. **Environment File**: 
   - Create a `.env` file at the root of the cloned directory.
   - Add your Pinata JWT token in the file:
     ```
     PINATA_JWT_TOKEN=your_token_here
     ```

## Usage

- Modify `pinata_post.py` to include your file path.
- Run the script with the command:
```
python pinata_post.py
```

## Requirements

- Python
- Requests and python-dotenv packages