from Crypto.Cipher import AES
import base64
import argparse

K_nodes = 'Skoltech 1234567'
K_tuples = '1234567 Skoltech'

encryption_nodes = AES.new(K_nodes)
encryption_tuples = AES.new(K_tuples)

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(s))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e))


parser = argparse.ArgumentParser()
parser.add_argument('graph_path', type=str, help='an graph path')
parser.add_argument('epsilon', type=float, help='an graph path')
graph_path = parser.parse_args().graph_path
eps = parser.parse_args().epsilon


def read_file(graph_path):
    f = open(graph_path, 'r')
    drafts = {}

    for line in f:
        line = line.strip().split(':')
        drafts[int(line[0])] = set()
        for element in line[1].strip().split(';'):
            if not element:
                continue
            vertex, dist = element.split(',')
            drafts[int(line[0])].add((int(vertex), int(dist)))
    return drafts

drafts = read_file(graph_path)
S = max(drafts.keys())
D = 0
for v in drafts:
    D = max(D, max([x[1] for x in drafts[v]]))
N = 2*D + 1
t = int(2. * S * S / eps) + 1
print 'S', S
print 'D', D
print 'N', N
print 't', t

def hash(vertex):
    return vertex % t

def prepare_to_encryption(v):
    v = str(v)
    if len(v) % 16 == 0:
        return v
    else:
        return v + " "*(16 - len(v)%16)

def write_crypto_file(graph_path, drafts):
    
    f = open(graph_path + '.crypto', 'w')
    for v in drafts.keys():
        word =   base64.b64encode(encryption_nodes.encrypt(prepare_to_encryption(v)))
        f.write(word)
        f.write(':::::')

        #hash_array = [base64.b64encode(encryption_tuples.encrypt(prepare_to_encryption(0))) for i in range(t)]
        hash_array = ['0' for i in range(t)]
        
        for dist in drafts[v]:
            new_dist = 2**(N - dist[1])
            #hash_array[hash(dist[0])] = base64.b64encode(encryption_tuples.encrypt(prepare_to_encryption(new_dist)))
            hash_array[hash(dist[0])] = str(new_dist) 

        for dist in hash_array:
            f.write(dist)
            f.write(';;;;;')
        f.write('\n')
    f.close()

write_crypto_file(graph_path, drafts)
