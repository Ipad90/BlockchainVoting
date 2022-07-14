from threading import Thread

import configparser
import socket
import subprocess
import sys

def send_stop_signal(port):
    print(f'Stopping service on port: {port}')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((socket.gethostbyname(socket.gethostname()), port))
        s.sendall('STOP'.encode())
    except:
        print(f'Failed to stop service on port: {port}')

    s.close()

if __name__ == '__main__':
    args = sys.argv[1:]
    config = configparser.ConfigParser()

    valid_processes = {
        '--all': [],
        '--tracker': [
            'tracker_server_started',
            'Tracker server',
            './Tracker/tracker.py',
            5154
        ],
        '--node': [
            'node_started',
            'Node',
            './Node/node.py',
            5153
        ]
    }

    if args:
        if args[0].lower() == 'start' or args[0].lower() == 'stop':
            config.read('config.ini')

            flag = '1'
            message = 'Started'

            if args[0].lower() == 'stop':
                flag = '0'
                message = 'Stopped'

            if '--all' in args:
                config.set('processes', 'tracker_server_started', flag)
                config.set('processes', 'node_started', flag)

                threads = [
                    Thread(target = send_stop_signal, args = (5153, )),
                    Thread(target = send_stop_signal, args = (5154, ))
                ]

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

                print(f'{message} all processes.')
            else:
                for arg in args:
                    if arg in valid_processes:
                        if flag == '1':
                            subprocess.call([
                                'python', f'{valid_processes[arg][2]}'
                            ])
                        else:
                            send_stop_signal(valid_processes[arg][3])
                        config.set('processes', valid_processes[arg][0], flag)
                        print(f"{message} process {valid_processes[arg][1]}.")

            with open('config.ini', 'w+') as cf:
                config.write(cf)
