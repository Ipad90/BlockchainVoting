from Node.client import Client
from Node.server import Server

from threading import Thread

import datetime
import json
import socket
import time
import logging

prefix = 'Node |'

"""
Sends a join network request to the tracker server

Args:
    server_host (str):
    server_port (int):
"""
def request_join_network(server_host, server_port) -> None:
    while True:
        print(f'{prefix} {datetime.datetime.now()} | Sending join network request')

        join_message = json.dumps({
            'request_type': 'request_join',
            'ip_address': server_host,
            'port': server_port
        })

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((socket.gethostbyname(socket.gethostname()), 5150))
            s.sendall(join_message.encode())

            try:
                response = s.recv(1024)
            except Exception as f:
                print(f'{prefix} {datetime.datetime.now()} | {f}')
            else:
                response = json.loads(response)
                print(f"{prefix} {datetime.datetime.now()} | Network join request {response['status']}")

                break
        except Exception as e:
            print(f'{prefix} {datetime.datetime.now()} | {e}')

        s.close()
        time.sleep(5)

if __name__ == '__main__':
    q = []

    server_host = ''
    server_port = 5151
    file_prefix = '1'

    client = Client(server_port,file_prefix)
    server = Server(server_host, server_port, file_prefix)
    
    request_join_network(server_host, server_port)

    threads = [
        Thread(target = client.get_peers, args = ()),
        Thread(target = client.sync_with_peers, args = ()),
        Thread(target = client.run_client, args = (q, )),
        Thread(target = server.run_server, args = (q, ))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
