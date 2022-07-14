import hashlib
import hmac
import json
import socket

def generate_hash(message):
    block_stringed = json.dumps(message, separators = (',', ':'))
    return hashlib.sha256(block_stringed.encode()).hexdigest()

if __name__ == '__main__':
    add_vote = {
        'headers': {
            'timestamp': 0
        },
        'tx_details': {
            'tx_type': 'add_vote',
            'election': '',
            'candidate': '',
            'voter_details': ''
        }
    }
    add_vote['headers']['tx_hash'] = generate_hash(add_vote)
    add_vote = json.dumps(add_vote)

    add_election = {
        'headers': {
            'timestamp': 300
        },
        'tx_details': {
            'tx_type': 'add_election',
            'election_details': {
                'election_name': 'Test Election',
                'candidates': [
                    'Apu Apustaja',
                    'Kry Kat'
                ],
                'start_timestamp': 0,
                'end_timestamp': 2147483647
            },
        }
    }
    add_election['headers']['tx_hash'] = generate_hash(add_election)
    add_election = json.dumps(add_election)

    view_tx = {
        'headers': {
            'tx_hash': '9d180739e38d2b5a7956fb1919a8b3cd2d80d7aaa5e54d6090516b9eee6f87df'
        },
        'tx_details': {
            'tx_type': 'view_tx'
        }
    }
    latest_tx = {
        'tx_details': {
            'tx_type': 'latest_tx'
        }
    }
    list_elections = json.dumps({
        'tx_details': {
            'tx_type': 'list_elections'
        }
    })
    request_results = json.dumps({
        'headers': {
            'tx_hash': '68319757087a0a9450a4cecbadb7398f8060c3dab018803d43ff2426f053d48c'
        },
        'tx_details': {
            'tx_type': 'request_results'
        }
    })

    # view_tx = json.dumps(view_tx)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostbyname(socket.gethostname()), 5151))
    s.sendall(request_results.encode())
    # s.sendall(json.dumps().encode())
    response = s.recv(1024)
    s.close()

    response = json.loads(response)
    print(response)

    #   FOR LIST ELECTIONS ONLY
    # for txid in response['tx_details']['election_txid_list']:
    #     view_tx_message = view_tx
    #     view_tx_message['headers']['tx_hash'] = txid
    #     view_tx_message = json.dumps(view_tx_message)

    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     s.connect((socket.gethostbyname(socket.gethostname()), 5151))
    #     s.sendall(view_tx_message.encode())
    #     tx_details = s.recv(1024)
    #     s.close()

    #     print(json.loads(tx_details))
        

