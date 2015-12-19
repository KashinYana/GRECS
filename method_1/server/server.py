# server.py 
import socket                                         
import time
import sys

import argparse

# create a socket object
serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

parser = argparse.ArgumentParser()
parser.add_argument('port', type=int, help='an port')
port = parser.parse_args().port

# bind to the port
serversocket.bind((host, port))                                  

# queue up to 5 requests
serversocket.listen(5)

def receive_file(file_id, clientsocket):
    print 'ready to recv file ' +  file_id
    f = open('graph/' + file_id, 'wb')
    l = clientsocket.recv(1024)
    while l:
        f.write(l)
        l = clientsocket.recv(1024)
    f.close()
    print "Done Receiving"
    clientsocket.send('Ok')                                           


def answer_query(file_id, u, v, clientsocket):
    f = open('graph/' + file_id, 'r')
    draft_u = None
    draft_v = None

    for line in f:
        line = line.strip().split(':::::')
        if len(line) >= 2:
            print line[0]
            if line[0] == u:
                draft_u = line[1]
            if line[0] == v:
                draft_v = line[1]

    print 'send draft_u'
    print 'send draft_v'
    
    if draft_u and draft_v:
        clientsocket.send(draft_u)
        clientsocket.send(draft_v)
    else:
        print 'Error'
        print 'draft_u', draft_u
        print 'draft_v', draft_v


while True:
    # establish a connection
    clientsocket, addr = serversocket.accept() 

    data = clientsocket.recv(1024)
    data = data.split()
    if len(data) > 0:
        if data[0] == 'f':
            receive_file(data[1], clientsocket)
        if data[0] == 'q':
            clientsocket.send('Ok')
            u = clientsocket.recv(1024)
            clientsocket.send('Ok')
            v = clientsocket.recv(1024)
            print 'u', u
            print 'v', v
            answer_query(data[1], u, v, clientsocket)
        if data[0] == 'e':
            print 'in exit'
            clientsocket.close()
            serversocket.close()
            sys.exit(0)
    clientsocket.close()
    
serversocket.close()