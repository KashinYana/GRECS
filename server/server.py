# server.py 
import socket                                         
import time
import sys

# create a socket object
serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 9974                     

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
        print 'recv ... '
        print l
        l = clientsocket.recv(1024)
    f.close()
    print "Done Receiving"
    clientsocket.send('Ok')                                           


def answer_query(file_id, u, v, clientsocket):
    f = open('graph/' + file_id, 'r')
    draft_u = {}
    draft_v = {}

    for line in f:
        line = line.strip().split(':')
        if line[0] == u or line[0] == v:
            for element in line[1].strip().split(';'):
                if not element:
                    continue
                vertex, dist = element.split(',')
                if line[0] == u:
                    draft_u[vertex]  = int(dist) 
                if line[0] == v:
                    draft_v[vertex]  = int(dist)  

    min_distance = False
    print 'draft_u', draft_u
    print 'draft_v', draft_v
    
    for candidate in draft_u:
        if candidate in draft_v:
            if not min_distance or draft_u[candidate] + draft_v[candidate] < min_distance:
                min_distance = draft_u[candidate] + draft_v[candidate]
    print 'min_distance', min_distance
    clientsocket.send(str(min_distance))


while True:
    # establish a connection
    clientsocket, addr = serversocket.accept() 

    data = clientsocket.recv(1024)
    print 'raw_data', data
    data = data.split()
    print 'data', data
    if len(data) > 0:
        print 'in if'
        if data[0] == 'f':
            print 'in file'
            receive_file(data[1], clientsocket)
        if data[0] == 'q':
            print 'in query'
            answer_query(data[1], data[2], data[3], clientsocket)
        if data[0] == 'e':
            print 'in exit'
            clientsocket.close()
            serversocket.close()
            sys.exit(0)

    clientsocket.close()
    print 'close'

serversocket.close()