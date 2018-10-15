import socket
import _thread
import helper
import sys

#parse command line
host_port = None
usage_message = 'Usage: $ python3 proxy.py -P <port_number>'
if len(sys.argv) > 2 and sys.argv[1] == '-P':
    try:
        host_port = int(sys.argv[2])
    except ValueError:
        print(usage_message)
        print("Invalid port number")
        quit()
else:
    print(usage_message)
    quit()

#Create a server socket listening on the specified port
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host_ip, host_port))
s.listen()
print('Proxy server start in device {name}, listening to {ip}:{port}'.format(name=host_name, ip=host_ip,
                                                                          port=host_port))

#Spawn a worker thread to handle the connection
def handler(conn, addr):
    request_recevied = conn.recv(65535)
    print('Server connected by', addr)
    data = helper.proxy(request_recevied)
    conn.sendall(data)
    conn.close()

while True:
    _thread.start_new_thread(handler, s.accept())
