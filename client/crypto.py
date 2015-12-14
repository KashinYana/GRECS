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
graph_path = parser.parse_args().graph_path


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

def prepare_to_encryption(v):
    v = str(v)
    if len(v) % 16 == 0:
        return v
    else:
        return v + " "*(16 - len(v)%16)

def write_crypto_file(graph_path, drafts):
    max_S = 0
    for draft in drafts:
        max_S = max(len(drafts[draft]), max_S)

    f = open(graph_path + '.crypto', 'w')
    for v in drafts.keys():
        word =   base64.b64encode(encryption_nodes.encrypt(prepare_to_encryption(v)))
        print 'v', '"', v, '"', word
        f.write(word)
        f.write(':::::')
        for dist in drafts[v]:
            tupl = str(dist[0]) + ',' + str(dist[1])
            f.write( base64.b64encode(encryption_tuples.encrypt(prepare_to_encryption(tupl))))
            f.write(';;;;;')
        f.write('\n')
    f.close()


write_crypto_file(graph_path, drafts)
