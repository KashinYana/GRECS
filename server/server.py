# server.py 
import socket                                         
import time

# create a socket object
serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 9988                                          

# bind to the port
serversocket.bind((host, port))                                  

# queue up to 5 requests
serversocket.listen(1)                                           

# establish a connection
clientsocket, addr = serversocket.accept() 


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


for i in range(1):     
    data = clientsocket.recv(1024)
    data = data.split()
    if data[0] == 'f':
        receive_file(data[1], clientsocket)

clientsocket.close()