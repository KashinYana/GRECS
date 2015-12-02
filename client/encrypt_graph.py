import argparse

parser = argparse.ArgumentParser()
parser.add_argument('graph_path', type=str, help='an graph path')
graph_path = parser.parse_args().graph_path

# client.py  
import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 9988

# connection to hostname on the port.
s.connect((host, port))


s.sendall("f " + graph_path.split('/')[-1])
# Receive no more than 1024 bytes
f = open(graph_path,'rb')

#Send file
l = f.read(1024)
print 'l = ', l
while l:
    print 'sending....'
    s.send(l)
    l = f.read(1024)

f.close()
print "Done Sending"
s.shutdown(socket.SHUT_WR)

status = s.recv(1024)                                     
print("status:" + status)