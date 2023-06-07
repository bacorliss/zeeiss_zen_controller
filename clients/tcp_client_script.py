#!/usr/bin/env python
# Code based on http://docs.python.org/release/2.5.2/lib/socket-example.html
     
import socket
import sys
import time
HOST = '127.0.0.1' #'127.0.0.1'
PORT = 1235

print type(PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    socket.close()
except:
    print "Socket was already closed, no need to close"
s.connect((HOST, PORT))
#s.send('-(121)acquire_experiment;;')
s.send('-load_config 20X_HM;-set_zstack_experiment;-acquire_experiment;; ')
#s.send('-(123)acquire_experiment;-(124)acquire_experiment;;')
print "Recieving data..."
while 1:
    str =  s.recv(1024)
    if len(str) <> 0:
        print  str + "  EOM"
        time.sleep(1)

s.settimeout(5)


