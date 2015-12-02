import argparse

parser = argparse.ArgumentParser()
parser.add_argument('graph_path', type=str, help='an graph path')
graph_path = parser.parse_args().graph_path

# client.py  
import socket

while True:
	try:
		# create a socket object
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

		# get local machine name
		host = socket.gethostname()                           

		port = 9974
		s.connect((host, port))
		print 'ready'
		line = raw_input()
		u, v = line.strip().split()
		s.sendall("q " + graph_path.split('/')[-1] + " " + u + " " + v)
		dist = s.recv(1024) 
		print 'dist ' + str(dist)
		s.close()
		print 'close'
	except:
		pass
