#!/usr/bin/env python
# Code based on http://docs.python.org/release/2.5.2/lib/socket-example.html
     
import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 1237
BUFFER_SIZE = 10  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()

print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    conn.send(data)  # echo
    #conn.
conn.close()
