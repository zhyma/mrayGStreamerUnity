import socket
import time

address = ('127.0.0.1', 233)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)
msg = 'test'

while True:
    data, addr = s.recvfrom(2048)
    if not data:
        print "client has exist"
        break
    print "received:", data, "from", addr
    #s.sendto(msg, address)

s.close()
