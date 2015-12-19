import argparse
from Crypto.Cipher import AES
import base64

K_nodes = 'Skoltech 1234567'
K_tuples = '1234567 Skoltech'

encryption_nodes = AES.new(K_nodes)
encryption_tuples = AES.new(K_tuples)

parser = argparse.ArgumentParser()
parser.add_argument('graph_path', type=str, help='an graph path')
parser.add_argument('port', type=int, help='an port')
graph_path = parser.parse_args().graph_path
port = parser.parse_args().port



def prepare_to_encryption(v):
    v = str(v)
    if len(v) % 16 == 0:
        return v
    else:
        return (v + " "*(16 - len(v)%16))


# client.py  
import socket

while True:
    if True:
        line = raw_input()
        if line == 'exit':
            break
        # create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        # get local machine name
        host = socket.gethostname()                           

        s.connect((host, port))

        u, v = line.strip().split()
        
        u = base64.b64encode(encryption_nodes.encrypt(prepare_to_encryption(u)))
        v = base64.b64encode(encryption_nodes.encrypt(prepare_to_encryption(v)))
        
        s.sendall("q " + graph_path.split('/')[-1])
        s.recv(1024) 
        s.sendall(u)
        s.recv(1024) 
        s.sendall(v)

        draft_u_cr = s.recv(1024) 
        draft_v_cr = s.recv(1024) 

        draft_u = {}
        draft_v = {}

        for el in draft_u_cr.split(';;;;;'):
            if el:
                el = base64.b64decode(el)
                el_enc = encryption_tuples.decrypt(el)
                vertex_dist = el_enc.strip().split(',')
                vertex, dist = vertex_dist[0], vertex_dist[1]
                draft_u[vertex] =  int(dist)
        for el in draft_v_cr.split(';;;;;'):
            if el:
                el = base64.b64decode(el)
                el_enc = encryption_tuples.decrypt(el)
                vertex_dist = el_enc.split(',')
                vertex, dist = vertex_dist[0], vertex_dist[1]
                draft_v[vertex] = int(dist)

        min_distance = False

        for candidate in draft_u:
            if candidate in draft_v:
                if not min_distance or draft_u[candidate] + draft_v[candidate] < min_distance:
                    min_distance = draft_u[candidate] + draft_v[candidate]

        print 'dist ' + str(min_distance)
        s.close()
        print 'close'
    
