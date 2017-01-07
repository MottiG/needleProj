import networkx as nx
import random

PERCENTS = 15   # percents of nodes in the sample
VERT_FILE = 'data/patents.txt'
EDGE_FILE = 'data/citations.txt'


print("Getting edges")
with open(EDGE_FILE,  mode='rb') as ef:
    next(ef)
    G = nx.read_edgelist(ef)


print("Getting vertices")
with open(VERT_FILE, encoding="utf8") as vf:
    vertices = [line.strip().split()[0] for line in vf.readlines()]
    vertices.pop(0)  # remove title


print('Adding vertices to  G')
G.add_nodes_from(vertices)
N = G.number_of_nodes()
num_of_desire_nodes = PERCENTS*N/100
print("number of nodes: ", N)
print("num_of_desire_nodes: ",num_of_desire_nodes)

print('Starting to Sample')
Gs = nx.Graph()  # sample of G
is_not_enough = True
while is_not_enough:
    rand = random.randint(0, N-1)
    node = G.nodes()[rand]
    neighbors = G[node].keys()
    if len(neighbors):
        neighbors_edges = [[node, neighbor] for neighbor in neighbors]
        Gs.add_edges_from(neighbors_edges)
    else:  # isolated node
        Gs.add_node(node)
    is_not_enough = Gs.number_of_nodes() < num_of_desire_nodes
print('Done Sampling')

gs_edges = [t[0]+' '+t[1] for t in Gs.edges()]

print('number of sampled nodes: ', Gs.number_of_nodes())
print('number of sampled edges: ', Gs.number_of_edges())
print('len of gs_edges: ', len(gs_edges))

print('Writing nodes_sample file')
with open('nodes_sample.txt', mode='wt', encoding='utf-8') as ns:
    ns.write('\n'.join(Gs.nodes()))

print('Writing edges_sample file')
with open('edges_sample.txt', mode='wt', encoding='utf-8') as es:
    es.write('\n'.join(gs_edges))

print('Done')
