import argparse
from Crypto.Cipher import AES
import base64
import math

K_nodes = 'Skoltech 1234567'
K_tuples = '1234567 Skoltech'

encryption_nodes = AES.new(K_nodes)
encryption_tuples = AES.new(K_tuples)

parser = argparse.ArgumentParser()
parser.add_argument('graph_path', type=str, help='an graph path')
parser.add_argument('port', type=int, help='an port')
parser.add_argument('N', type=int, help='N')
graph_path = parser.parse_args().graph_path
port = parser.parse_args().port
N = parser.parse_args().N

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

        crypto_dist = s.recv(1024) 
        #crypto_dist = base64.b64decode(crypto_dist)
        #crypto_dist = encryption_tuples.decrypt(crypto_dist)
        crypto_dist = int(crypto_dist)

        dist = 2*N - math.log(crypto_dist, 2)

        print 'dist ' + str(dist)
        s.close()
        print 'close'
    
