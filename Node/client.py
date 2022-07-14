from Block.block import Block

import configparser
import datetime
import json
import socket
import logging
import time

"""
The client component of the node module
"""
class Client():
    """
    Args:
        server_port (int):
        file_prefix (str):
    """
    def __init__(self, server_port, file_prefix):
        self.block = Block(file_prefix)
        self.server_details = [
            socket.gethostbyname(socket.gethostname()),
            server_port
        ]
        self.tracker_server = socket.gethostbyname(socket.gethostname())
        self.peers = []
        self.prefix = 'Client |'

    """
    Get peers from the tracker server
    """
    def get_peers(self):
        #   TODO: DHT to get peers from other peers

        request_peer_list = {
            'request_type': 'request_list'
        }
        request_peer_list = json.dumps(request_peer_list)

        while True:
            print(f'{self.prefix} {datetime.datetime.now()} | Requesting nodes from tracker server')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                s.connect((self.tracker_server, 5150))
                s.settimeout(3)
                s.sendall(request_peer_list.encode())

                try:
                    peer_list = s.recv(1024)
                except Exception as f:
                    print(f'{self.prefix} {datetime.datetime.now()} | {f}')
                else:
                    peer_list = peer_list.decode()
                    peer_list = json.loads(peer_list)
                    peer_list = peer_list['peer_list']

                    for peers in peer_list:
                        if peers[0] == self.server_details[0] and int(peers[1]) == int(self.server_details[1]):
                            peer_list.remove(peers)

                    self.peers = peer_list
                print(f"{self.prefix} {datetime.datetime.now()} | Current peers are: {self.peers}")
            except Exception as e:
                print(f'{self.prefix} {datetime.datetime.now()} | Failed to connect to Tracking server')
                print(f'{self.prefix} {datetime.datetime.now()} | {e}')

            s.close()
            time.sleep(10)

    """
    Sync blockchain data with other peers
    """
    def sync_with_peers(self):
        print(f'{self.prefix} {datetime.datetime.now()} | Syncing with peers')
        peer_details = []
        most_complete_peer = {}
        txids_to_get = []
        own_details = {
            'connection': self.server_details
        }
        request_index_length = {
            **own_details,
            'peer_msg': 'index_length'
        }
        request_index_length = json.dumps(request_index_length)
        request_index_contents = {
            **own_details,
            'peer_msg': 'index_contents'
        }
        request_index_contents = json.dumps(request_index_contents)
        request_tx_details = {
            'headers': {
                'tx_hash': ''
            },
            'tx_details': {
                'tx_type': 'view_tx'
            }
        }

        while True:
            for peers in self.peers:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    s.connect((peers[0], int(peers[1])))
                    s.sendall(request_index_length.encode())

                    try:
                        response = s.recv(1024)
                    except Exception as f:
                        print(f'{self.prefix} {datetime.datetime.now()} | {f}')
                    else:
                        response = response.decode()
                        response = json.loads(response)
                        response = response['response']

                        peer_details.append({
                            'peer': peers,
                            'index_length': int(response)
                        })
                except Exception as e:
                    print(f'{self.prefix} {datetime.datetime.now()} | {e}')

                s.close()

            if peer_details:
                most_complete_peer = max(peer_details, key = lambda x: x['index_length'])
                print(f'{self.prefix} {datetime.datetime.now()} | Most complete peer: {most_complete_peer}')
                break

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((most_complete_peer['peer'][0], most_complete_peer['peer'][1]))
            s.sendall(request_index_contents.encode())

            try:
                response = s.recv(1024)
            except Exception as f:
                print(f'{self.prefix} {datetime.datetime.now()} | {f}')
            else:
                response = response.decode()
                response = json.loads(response)
                response = response['response']
                txids_to_get = self.compare_index(response)
        except Exception as e:
            print(f'{self.prefix} {datetime.datetime.now()} | {e}')

        s.close()

        for txid in txids_to_get:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            message = request_tx_details

            txid = txid.strip()
            txid = txid.split('=')

            message['headers']['tx_hash'] = txid[0]
            message = json.dumps(message)

            try:
                s.connect((most_complete_peer['peer'][0], most_complete_peer['peer'][1]))
                s.sendall(message.encode())

                try:
                    response = s.recv(1024)
                except Exception as f:
                    print(f'{self.prefix} {datetime.datetime.now()} | {f}')
                else:
                    response = response.decode()
                    response = json.loads(response)
                    response = response['tx_details']['specified_tx_details']

                    if self.block.validate_transaction(response):
                        if not self.block.check_duplicate_transaction(response):
                            print(f"{self.prefix} {datetime.datetime.now()} | Synced transaction {response['headers']['tx_hash']}")
                            self.block.create_transaction(response)
                    else:
                        print(f"{self.prefix} {datetime.datetime.now()} | Transaction {response['headers']['tx_hash']} Invalid")
            except Exception as e:
                print(f'{self.prefix} {datetime.datetime.now()} | {e}')

            s.close()

    """
    Args:
        received_index (list):

    Returns:
        list: A list of transactions to get
    """
    def compare_index(self, received_index: list) -> list:
        own_index = self.block.get_index()
        
        return list(set(received_index) - set(own_index))

    """
    Runs the client process

    Args:
        queue (list): Queue of transactions to send out
    """
    def run_client(self, queue: list):
        print(f'{self.prefix} {datetime.datetime.now()} | Process started')

        while True:
            if queue:
                for items in queue:
                    message = json.dumps(items)

                    for peers in self.peers:
                        print(f'{self.prefix} {datetime.datetime.now()} | Sending to {peers[0]}|{peers[1]}: {message}')

                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                        try:
                            s.connect((peers[0], int(peers[1])))
                            s.settimeout(5)
                            s.sendall(message.encode())
                            s.close()
                        except Exception as e:
                            print(f'{self.prefix} {datetime.datetime.now()} | Unable to send to peer: {peers[0]}:{peers[1]}')
                            print(f'{self.prefix} {datetime.datetime.now()} | Reason: {e}')

                            # TODO: REMOVE FAILED PEER
                        else:
                            print(f'{self.prefix} {datetime.datetime.now()} | Sent to {peers[0]}:{peers[1]}')
                    queue.remove(items)

            time.sleep(5)
