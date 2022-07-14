from Block.block import Block

from threading import Thread

import configparser
import datetime
import json
import socket
import logging

"""
The server component of the node module.
"""
class Server():
    """
    Args:
        host (str): The IP address to bind the server process.
        port (int): The port number to bind the server process.
        file_prefix (str): 
    """
    def __init__(self, host, port, file_prefix):
        self.block = Block(file_prefix)
        self.host = host
        self.port = port
        self.still_running = True
        self.prefix = 'Server |'

    """
    Runs the server process

    Args:
        queue (list): Queue to store transactions for client process to send out.
    """
    def run_server(self, queue: list) -> None:
        print(f'{self.prefix} {datetime.datetime.now()} | Proces started on: {socket.gethostbyname(socket.gethostname())}:{self.port}')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind((self.host, self.port))
        s.listen(32)

        while True:
            conn, addr = s.accept()

            try:
                Thread(target = self.request_filter, args = (queue, conn, addr, )).start()
            except Exception as e:
                print(f'{self.prefix} {datetime.datetime.now()} | {e}')

        s.close()

    """
    Filters out the request 
    Args:
        queue (list):
        conn:
        addr:
    """
    def request_filter(self, queue: list, conn: socket, addr: tuple) -> None:
        with conn:
            try:
                data = conn.recv(1024)
            except Exception as e:
                print(f'{self.prefix} {datetime.datetime.now()} | {e}')
            else:
                if data:
                    data = data.decode()
                    data = data.strip()
                    data = json.loads(data)

                    print(f'{self.prefix} {datetime.datetime.now()} | From {addr[0]}: {data}')

                    if 'peer_msg' in data:
                        data = self.peer_request_handler(data)

                    if 'tx_details' in data:
                        data = self.tx_request_handler(data)

                        if data['tx_details']['status'] == 'approved':
                            queue.append(data)

                conn.sendall(json.dumps(data).encode())
            conn.close()

    """
    Handles transaction requests related to Blockchain module

    Args:
        message (dict): A message containing the transaction type and the required 
            parameters for the transaction type

    Returns:
        dict: The response message to be sent back to the sender
    """
    def tx_request_handler(self, message: dict) -> dict:
        if 'tx_details' in message:
            if 'tx_type' in message['tx_details']:
                match message['tx_details']['tx_type']:
                    case 'add_election' | 'add_vote':
                        if not self.block.check_duplicate_transaction(message):
                            if self.block.validate_transaction(message):
                                message['tx_details']['status'] = 'approved'
                                self.block.create_transaction(message)
                            else:
                                message['tx_details']['status'] = 'rejected'
                        print(f"{self.prefix} {datetime.datetime.now()} | Transaction {message['headers']['tx_hash']} {message['tx_details']['status']}")

                    case 'latest_tx':
                        latest_tx_details = self.block.get_latest_transaction()

                        if latest_tx_details:
                            message['tx_details']['specified_tx_details'] = latest_tx_details
                        message['tx_details']['status'] = 'non queue'

                    case 'view_tx':
                        specified_tx_details = self.block.get_transaction(message['headers']['tx_hash'])

                        if specified_tx_details:
                            message['tx_details']['specified_tx_details'] = json.loads(specified_tx_details)
                        message['tx_details']['status'] = 'non queue'

                    case 'list_elections':
                        message['tx_details']['election_txid_list'] = self.block.get_txids_of_type('add_election')
                        message['tx_details']['status'] = 'non queue'

                    case 'list_votes':
                        message['tx_details']['election_txid_list'] = self.blocks.get_transactions_related_to_txid(None, None)
                        message['tx_details']['status'] = 'non queue'

                    case 'request_results':
                        message['tx_details']['results'] = self.block.tally_votes_of_election(message['headers']['tx_hash'])
                        message['tx_details']['status'] = 'non queue'

                    case _:
                        message['tx_details']['status'] = 'rejected'
            else:
                message['tx_details']['status'] = 'rejected'
        else:
            message['tx_details'] = {}
            message['tx_details']['status'] = 'rejected'

        return message

    """
    Handles requests from other Nodes

    Args:
        message (dict): A message containing the transaction type and the required 
            parameters for the transaction type

    Returns:
        dict: The response message to be sent back to the sender
    """
    def peer_request_handler(self, message: dict) -> dict:
        match message['peer_msg']:
            case 'index_length':
                message['response'] = self.block.get_index(count = True)

            case 'index_contents':
                message['response'] = self.block.get_index()

            case 'request_tx':
                requested_transactions = []

                if 'tx_details' in message['peer_msg']:
                    for txid in message['peer_msg']:
                        requested_transactions.append(self.block.get_transaction(txid))

                message['response'] = requested_transactions

            case _:
                message['response'] = []

        return message
