#!/usr/bin/python3
import socket
import struct

# initialize a TCP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to host and port
server_ip = '35.230.71.159'
server_port = 8181
s.connect((server_ip, server_port))
print('[info] Successfully connected to host {}:{}'.format(server_ip, server_port))

# message to send
list = [
    11, 
    4, '3+12', 
    6, '1+12/3',
    4, '5-10',
    5, '3+5*3',
    2, '12',
    7, '(1+3)*2',
    7, '3-(2+4)',
    9, '3+12*14-3',
    20, '1+12/3+4-5+7-6*31+12',
    11, '(1+2)*(3+4)',
    21, '(((-11+6)*5+6)*9+7)/4'
]

# helper function to receive all data, 16 bytes per time
def recvall(socket):
    buffer_size = 16
    data = b''
    while True:
        packet = socket.recv(buffer_size)
        data += packet
        # either 0 or EOF
        if len(packet) < buffer_size:
            break
    return data

def build_message(list):
    byte_list = [];
    for index, elem in enumerate(list):
        if (index == 0 or index % 2 == 1):
            byte_list.append(struct.pack('>H', elem))
        else:
            byte_list.append(elem.encode('utf-8'))
    return b''.join(byte_list)

# send message to server over socket
s.sendall(build_message(list) + '\n'.encode('utf-8'))
print('[info] Client sent:', build_message(list) + "\n".encode('utf-8'))
# receive data
resp = recvall(s)
print('[info] response from server:', resp)

# close socket to send EOF to server
s.close()
