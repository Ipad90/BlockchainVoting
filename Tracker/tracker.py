from threading import Thread

import configparser
import datetime
import json
import socket
import time
import logging
import os

"""
The node tracker module.
"""
class Tracker():
    """
    Args:
        host (str): The IP address to bind the server process.
        port (int): The port to bind the server process.
        file_prefix (str): 
    """
    def __init__(self):
        self.host = ''
        self.port = 5150
        self.nodes = []
        self.prefix = 'Tracker |'

    """
    Loads nodes from a previous session (if exists).
    """
    def load_existing_nodes(self) -> None:
        with open('Tracker/tracker.dat', 'r') as f:
            for nodes in f:
                nodes = nodes.strip()
                self.nodes.append(nodes.split(':'))

    """
    Add new nodes to the tracked nodes list.
    Checks if the new node is a duplicate node or not before adding.

    Args:
        ip_address (str): The IP address of the new node to be added.
        port (int): The port number of the new node to be added.
    """
    def add_nodes(self, ip_address: str, port: int) -> None:
        if self.nodes:
            for node in self.nodes:
                if ip_address != node[0] or int(port) != int(node[1]):
                    print(f'{self.prefix} {datetime.datetime.now()} | (If For) Adding {ip_address}:{port}')
                    self.nodes.append([
                        ip_address, port
                    ])

                    with open('Tracker/tracker.dat', 'a') as f:
                        f.write(f'{ip_address}:{port}\n')
                    break
                else:
                    print(f'{self.prefix} {datetime.datetime.now()} | Node rejected')
                    break
        else:
            print(f'{self.prefix} {datetime.datetime.now()} | (Else) Adding {ip_address}:{port}')
            self.nodes.append([
                ip_address, port
            ])

            with open('Tracker/tracker.dat', 'a') as f:
                f.write(f'{ip_address}:{port}\n')

    """
    Removes nodes from the tracked nodes list.

    Args:
        ip_address (str): The IP address of the node to be removed.
        port (int): The port number of the node to be removed.
    """
    def remove_nodes(self, ip_address: str, port: int) -> None:
        self.nodes.remove([
            ip_address, port
        ])

        with open('Tracker/tracker.dat', 'w') as f:
            for node in self.nodes:
                f.write(f'{node[0]}:{node[1]}\n')

    """
    Checks the nodes in the tracked nodes list to see whether the node is still active or not.
    """
    def check_nodes(self) -> None:
        ping_message = {
            'tracker_server_ping_message': 'hi'
        }

        while True:
            for node in self.nodes:
                print(f'{self.prefix} {datetime.datetime.now()} | Checking {node[0]}:{node[1]}')

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    s.connect((node[0], int(node[1])))
                    s.sendall(json.dumps(ping_message).encode())
                    s.settimeout(3)
                except Exception as e:
                    print(f'{self.prefix} {datetime.datetime.now()} | Removing {node[0]}:{node[1]}')
                    self.remove_nodes(node[0], node[1])
                else:
                    print(f'{self.prefix} {datetime.datetime.now()} | Keeping {node[0]}:{node[1]}')
                s.close()

            time.sleep(5)

    """
    Runs the tracker server process.
    A new thread is created whenever a new connection is received.
    """
    def run_server(self) -> None:
        print(f'{self.prefix} {datetime.datetime.now()} | Process started on: {socket.gethostbyname(socket.gethostname())}:{self.port}')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind((self.host, self.port))
        s.listen(32)

        while True:
            conn, addr = s.accept()

            try:
                Thread(target = self.request_filter, args = (conn, addr, )).start()
            except Exception as e:
                print(f'{self.prefix} {datetime.datetime.now()} | {e}')

        s.close()

    """
    Args:
        conn (socket): The socket 
        addr (tuple):
    """
    def request_filter(self, conn: socket, addr: tuple) -> None:
        with conn:
            try:
                data = conn.recv(1024)
            except Exception as e:
                print(f'{self.prefix} {datetime.datetime.now()} | {e}')
            else:
                if data:
                    data = data.decode()
                    data = data.strip()

                    conn.sendall(self.request_handler(addr, data).encode())
                conn.close()

    """
    Handles node requests.

    Args:
        addr (tuple):
        message (dict):

    Returns:
        dict:
    """
    def request_handler(self, addr , message: dict) -> dict:
        message = json.loads(message)

        match message['request_type']:
            case 'request_join':
                self.add_nodes(addr[0], message['port'])
                message['status'] = 'approved'
                print(f"{self.prefix} {datetime.datetime.now()} | Join request of {addr[0]}:{message['port']} {message['status']}")

            case 'request_list':
                message['status'] = 'approved'
                message['peer_list'] = self.nodes
                print(f"{self.prefix} {datetime.datetime.now()} | List request of {addr[0]} {message['status']}")

            case _:
                message['status'] = 'rejected'
                print(f"{self.prefix} {datetime.datetime.now()} | Unknown request of {addr[0]} {message['status']}")

        return json.dumps(message)

if __name__ == '__main__':
    tracker = Tracker()
    tracker.load_existing_nodes()

    threads = [
        Thread(target = tracker.run_server, args = ()),
        Thread(target = tracker.check_nodes, args = ())
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
