import math
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('graph_path', type=str, help='an graph path')
parser.add_argument('--alpha', type=float, help='an alpha')

graph_path = parser.parse_args().graph_path
alpha = parser.parse_args().alpha


def read_graph(graph_path):
	graph = {}

	f = open(graph_path, 'r')
	for line in f:
		if line and line[0] == '#':
			continue

		v, u = map(int, line.strip().split())
		if v in graph:
			graph[v].add(u)
		else:
			graph[v] = set([u])

		if u in graph:
			graph[u].add(v)
		else:
			graph[u] = set([v])

	return graph

graph = read_graph(graph_path)

sigma = int(len(graph)**(2./(alpha + 1)))
lamb = int(math.log(len(graph), 2))

print graph
print sigma
print lamb

def bfs(graph, s):
	distanses = {}
	for vertex in graph.keys():
		if vertex in s:
			distanses[vertex] = (vertex, 0)
		else:
			distanses[vertex] = False

	import Queue
	q = Queue.Queue()
	for i in s:
	    q.put(i)

	while not q.empty():
	    vertex = q.get()
	    for neigb in graph[vertex]:
	    	if not distanses[neigb]:
	    		distanses[neigb] = (distanses[vertex][0], distanses[vertex][1] + 1)
	    		q.put(neigb)
	return distanses


def calc_das_sarma_oracle(graph, sigma, lamb):
	vertexes = graph.keys()
	drafts = {}
	for vertex in vertexes:
		drafts[vertex] = set()

	for round_id in range(sigma):
		S = []
		for i in range(lamb):
			S.append(set(random.sample(vertexes, 2**i)))
		print S
		for s in S:
			distanses = bfs(graph, s)
			for vertex in vertexes:
				if distanses[vertex]:
					drafts[vertex].add(distanses[vertex])
	return drafts


drafts = calc_das_sarma_oracle(graph, sigma, lamb)

f = open(graph_path + '.draft', 'w')
for v in drafts.keys():
	f.write(str(v))
	f.write(':')
	for dist in drafts[v]:
		f.write(str(dist[0]))
		f.write(',')
		f.write(str(dist[1]))
		f.write(';')
	f.write('\n')
f.close()