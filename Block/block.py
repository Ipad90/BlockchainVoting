import base64
import hashlib
import hmac
import json
import os
import sys
import time
import logging

"""
The blockchain module
"""
class Block():
    """
    Args:
        file_prefix (str): The file prefix of the blockchain storage directory
    """
    def __init__(self, file_prefix: str):
        self.file_prefix = file_prefix
        self.prefix = 'Block |'

        self.file_dir = self.get_storage_directory()

    """
    Checks duplicate transactions by searching for the transaction specified

    Args:
        transaction (dict): Transaction to check if duplicate

    Returns:
        bool: A boolean value on whether the transaction is a duplicate or not
    """
    def check_duplicate_transaction(self, transaction: dict) -> bool:
        with open(f'{self.file_dir}/blk_index.dat', 'rb') as f:
            for lines in f:
                lines = lines.decode()
                lines = lines.strip()
                lines = lines.split('=')

                if lines[0] == transaction['headers']['tx_hash']:
                    with open(f'{self.file_dir}/{lines[1]}', 'rb') as r:
                        for transactions in r:
                            transactions = transactions.strip()
                            transactions = transactions.decode()
                            jsoned_transactions = json.loads(transactions)

                            if transaction['headers']['tx_hash'] == jsoned_transactions['headers']['tx_hash']:
                                return True
        return False

    """
    Checks the validity of the transaction by the SHA256 cryptographic hash

    Args:
        data (dict): Transaction to be validated

    Returns:
        bool: A boolean value on whether the transaction is valid or not
    """
    def validate_transaction(self, data: dict) -> bool:
        validity = False

        original_hash = data['headers']['tx_hash']
        del data['headers']['tx_hash']

        if 'status' in data['tx_details']:
            del data['tx_details']['status']

        block_stringed = json.dumps(data, separators = (',', ':'))
        regenerated_hash = hashlib.sha256(block_stringed.encode()).hexdigest()
        
        if regenerated_hash != original_hash:
            block_stringed = json.dumps(data)
            alternate_regenerated_hash = hashlib.sha256(block_stringed.encode()).hexdigest()

            if alternate_regenerated_hash == original_hash:
                validity = True
        else:
            validity = True

        data['headers']['tx_hash'] = original_hash

        return validity

    """
    Get the index file's contents or get the length of the index file depending on the parameter set

    Args:
        count (bool): Sets the return value to the length of the index file instead of the 
            contents if true (default is False)
    
    Returns:
        list: A list of the index entries
        int: The amount of index entries
    """
    def get_index(self, count = False) -> list | int:
        index = []

        with open(f'{self.file_dir}/blk_index.dat', 'rb') as f:
            for lines in f:
                lines = lines.strip()
                lines = lines.decode()
                index.append(lines)

        if count:
            index = len(index)

        return index

    """
    Get the transaction details of the specified transaction ID

    Args:
        txid (str): The transaction ID of the transaction to be found

    Returns:
        dict: The specified transaction's details, or blank if no transaction by that 
            transaction ID is found
    """
    def get_transaction(self, txid: str) -> dict:
        with open(f'{self.file_dir}/blk_index.dat', 'rb') as f:
            for lines in f:
                lines = lines.decode()
                lines = lines.strip()
                lines = lines.split('=')

                if lines[0] == txid:
                    with open(f'{self.file_dir}/{lines[1]}', 'rb') as r:
                        for transactions in r:
                            transactions = transactions.strip()
                            transactions = transactions.decode()
                            jsoned_transactions = json.loads(transactions)

                            if txid == jsoned_transactions['headers']['tx_hash']:
                                return transactions
        return {}

    """
    Gets the latest transaction by selecting the transaction with the largest unix timestamp

    Returns:
        dict: The latest transaction's details
    """
    def get_latest_transaction(self) -> dict:
        topmost_file = self.get_topmost_blk_file()
        blocks = []

        with open(f"{topmost_file['dir']}/{topmost_file['file']}", 'rb') as block_file:
            for block in block_file:
                block = block.decode()
                block = block.strip()
                blocks.append(json.loads(block))

        return max(blocks, key = lambda x: x['headers']['timestamp'])

    """
    Gets transactions of a certain type

    Args:
        tx_type (str): The type of transaction

    Returns:
        list: A list of transactions based on the type specified
    """
    def get_txids_of_type(self, tx_type: str) -> list:
        txids = []

        with open(f'{self.file_dir}/blk_index.dat', 'rb') as f:
            for lines in f:
                lines = lines.decode()
                lines = lines.strip()
                lines = lines.split('=')

                if lines[2] == tx_type:
                    txids.append(lines[0])

        return txids

    """
    Gets transactions related to the specified transaction ID

    Args:
        txid (str): The related transaction's transaction ID

    Returns:
        list: A list of transactions related to the specified transaction ID
    """
    def get_transactions_related_to_txid(self, txid):
        txids = []

        with open(f'{self.file_dir}/blk_index.dat', 'rb') as f:
            for lines in f:
                lines = lines.decode()
                lines = lines.strip()
                lines = lines.split('=')

                if len(lines) == 4:
                    if lines[3] == txid:
                        txids.append(lines[0])

        return txids

    """
    Tallies the votes of the specified election

    Args:
        election_txid (str):

    Returns:
        dict:
    """
    def tally_votes_of_election(self, election_txid):
        result = {}

        election_candidates = self.get_transaction(election_txid)
        election_candidates = json.loads(election_candidates)

        if election_candidates['tx_details']['tx_type'] == 'add_election':
            votes = self.get_transactions_related_to_txid(election_txid)

            for candidate in election_candidates['tx_details']['election_details']['candidates']:
                result[candidate] = 0

            for vote in votes:
                vote = self.get_transaction(vote)
                vote = json.loads(vote)

                result[vote['tx_details']['candidate']] = result[vote['tx_details']['candidate']] + 1

        return result

    """
    Creates a transaction

    Args:
        data (dict): The transaction's data
    """
    def create_transaction(self, data: dict) -> None:
        file_details = self.get_topmost_blk_file()
        stringed_data = json.dumps(data)

        with open(f"{file_details['dir']}/{file_details['file']}", 'ab') as f:
            byte_data = self.string_to_bytes(stringed_data)

            f.write(byte_data)
            f.write(b'\n')

        with open(f"{file_details['dir']}/blk_index.dat", 'ab') as f:
            stringed_data = f"{data['headers']['tx_hash']}={file_details['file']}={data['tx_details']['tx_type']}"

            if 'election' in data['tx_details']:
                stringed_data = f"{stringed_data}={data['tx_details']['election']}"

            byte_data = self.string_to_bytes(stringed_data)

            f.write(byte_data)
            f.write(b'\n')

    """
    Generates a unix timestamp based on the current date

    Returns:
        int: Unix timestamp with milliseconds
    """
    def generate_timestamp(self) -> int:
        return int(time.time() * 1000)

    """
    Gets the blockchain data storage directory

    Returns:
        str: The storage directory's path
    """
    def get_storage_directory(self) -> str:
        root_path = os.path.dirname(os.path.abspath('main.py'))
        file_path = f'{root_path}/Block Storage {self.file_prefix}'

        if not os.path.isdir(file_path):
            os.mkdir(file_path)
            index_file = os.path.join(file_path, 'blk_index.dat')
            f = open(index_file, 'wb')
            f.close()

        return file_path

    """
    Gets the topmost block storage file. For example, a directory containing:
    - blk0.dat
    - blk1.dat
    - blk2.dat
    The path of blk2.dat is retrieved as it is the topmost file

    Returns:
        dict: The directory and name of the topmost file
    """
    def get_topmost_blk_file(self) -> dict:
        files = os.listdir(self.file_dir)
        files.remove('blk_index.dat')
        file_name = ''

        if files == []:
            file_name = 'blk0.dat'
        else:
            files.sort()
            file_name = files[-1]
        
        return {
            'dir': self.file_dir,
            'file': file_name
        }

    def string_to_bytes(self, data) -> bytes:
        return bytes(data, encoding = 'utf8')

    def bytes_to_string(self, data) -> str:
        return data.decode('utf-8')
