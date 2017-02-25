from collections import defaultdict
import igraph

try:
   import cPickle as pickle
except:
   import pickle
import os

__author__ = 'slouis'
'''
This file creates the citation graph, as igraph object.

Inputs:
The file access both citation file (edges) and patents file, read the file directly (once) and creates the graph.

Outputs:
pickled igraph file

'''

project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..','..'))
input_dir = os.path.join(project_dir, 'data', 'raw')
output_dir = os.path.join(project_dir, 'data', 'processed','citation graph')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
citing_null = defaultdict(int)
cited_by_null = defaultdict(int)

#Reading the files
print("Loading the data")
VERT_FILE_PATH = os.path.join(input_dir, 'patents.txt')
EDGE_FILE_PATH = os.path.join(input_dir, 'citations.txt')

LIMIT_NUM_ROWS =  float("inf") #

print("reading edges")
G = igraph.Graph.Read_Ncol(EDGE_FILE_PATH, directed=False)

print("Loading vertices")
with open(VERT_FILE_PATH, mode='r',encoding='utf8') as vf:
    vertices_set = set()
    next(vf)
    row_counter = 0
    for line in vf:
        if row_counter % 100000 == 0 : print(row_counter)
        row_counter +=1
        ptidString = line.strip().split()[0]

        vertices_set.add(ptidString)
        if row_counter >= LIMIT_NUM_ROWS:
            break
    vcount = G.vcount()
    vertices_set = vertices_set - set(G.vs.get_attribute_values("name"))
    G.add_vertices(len(vertices_set))
    G.vs[range(vcount, vcount + len(vertices_set) - 1)]["name"] = list(vertices_set)

print("deleting None edges")
G.delete_vertices(G.vs.select(name = "None"))

## FOR MORE GRAPH FILE FORMAT SEE : http://igraph.org/python/doc/tutorial/tutorial.html#igraph-and-the-outside-world
# G.save(os.path.join(output_dir, 'citationGraph_'+ str(row_counter)+'.graph'), format="gml")

print("saving to file")
pickle.dump(G,open(os.path.join(output_dir, 'citationGraph'+'.pickle'),'wb'))