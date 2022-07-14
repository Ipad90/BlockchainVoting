import configparser
import os

if __name__ == '__main__':
    block = Block()
    config = configparser.ConfigParser()

    config['block'] = {
        'size': 128
    }
    config['ports'] = {
        'tracker': 5150,
        'node': 5153
    }
    config['processes'] = {
        'tracker_server_started': 1,
        'node_started': 1,
        'node_listen_only': 0
    }

    with open('config.ini', 'w') as cf:
        config.write(cf)
