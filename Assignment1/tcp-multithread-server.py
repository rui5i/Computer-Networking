#!/usr/bin/python3
import socket
import time
import _thread
import struct
import calculator

# TODO
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8181

# initialize a TCP socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind socket to host IP and port
s.bind((host_ip, host_port))
# listen up to 5 pending connections
s.listen(5)
print('[info] Server is listening on {}:{}...\n'.format(host_ip, host_port))

# get current time on server
def now():
    return time.ctime(time.time())

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

# helper function to build response message
def build_message(list):
    byte_list = [];
    for index, elem in enumerate(list):
        if (index == 0 or index % 2 == 1):
            byte_list.append(struct.pack('>H', elem))
        else:
            byte_list.append(elem.encode('utf-8'))
    return b''.join(byte_list)

# event handler
def handler(conn):
    response_list = []
    raw_message = recvall(conn)
    print('[info] Server received raw_message:', raw_message)
    exp_count = struct.unpack('>H', raw_message[0:2])[0]
    response_list.append(exp_count)
    start = 2
    while exp_count > 0:
        exp_len = struct.unpack('>H', raw_message[start:start + 2])[0]
        start += 2
        exp_content = raw_message[start:start + exp_len].decode('utf-8')
        exp_result = str(calculator.calculate(exp_content))
        response_list.append(len(exp_result))
        response_list.append(exp_result)
        start += exp_len
        exp_count -= 1
    # send response
    print('[info] response list to send:', response_list)
    conn.sendall(build_message(response_list))
    print('[info] message sent:', build_message(response_list))
    conn.close()

# multithreaded processing
while True:
    conn, addr = s.accept()
    print('[info] Server got connected by {} at {}'.format(addr, now()))
    _thread.start_new(handler, (conn,))
