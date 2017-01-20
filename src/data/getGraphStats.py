__author__ = 'slouis'
'''
This file reads in/out degree distributions of the citation graph.
The nodes are from both files: patent.txt & citations.txt files (to ensure we have also nodes of degree 0.

Outputs:
inDegreeDistributions <LIMIT_NUM_ROWS>.pickle - dictionary of in-degrees (key = patentID, val = inDegree)
outDegreeDistributions <LIMIT_NUM_ROWS>.pickle - dictionary of out-degrees (key = patentID, val = outDegree)
inDegreeDistributions <LIMIT_NUM_ROWS>.png - plot of the in-degree distribution
inDegreeDistributions <LIMIT_NUM_ROWS>.png - plot of the out-degree distribution
'''
from pygraph.classes.digraph import digraph
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import operator
try:
   import cPickle as pickle
except:
   import pickle
import os
from numpy import linspace as lrange

# plot histogram of the degree distribution and save to file
def plotDegrees(degrees, title = "degree distribution", ifShow = False, fileName = "", numOfBins = 100):
    print( Counter(degrees).most_common(10))
    fig = plt.figure()
    plt.hist(list(degrees),bins=lrange(min(degrees), max(degrees), numOfBins))
    plt.xlabel('degree')
    plt.yscale('log')
    plt.ylabel('log frequency')
    plt.title(title)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, max(degrees))
    if ifShow : plt.show()
    if len(fileName): plt.savefig(fileName+'.png',dpi=400)
    plt.clf()


project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'raw')
output_dir = os.path.join(project_dir, 'data', 'processed')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#Reading the files
print("Loading the data")
VERT_FILE_PATH = os.path.join(input_dir, 'patents.txt')
EDGE_FILE_PATH = os.path.join(input_dir, 'citations.txt')

LIMIT_NUM_ROWS = float("Inf")
gr = digraph()

print("Loading vertices")
with open(VERT_FILE_PATH, mode='r', encoding='utf-8') as vf:
    next(vf)
    row_counter = 0
    for line in vf:
        row_counter +=1
        gr.add_node(line.strip().split()[0])
        if row_counter >= LIMIT_NUM_ROWS:
            break

print("reading edges")
with open(EDGE_FILE_PATH,  mode='r', encoding='utf-8') as ef:
    next(ef)
    row_counter = 0
    for edgeRow in ef:
        if row_counter % 10000 == 0 : print(row_counter)
        row_counter +=1
        edge = edgeRow.split()
        # if edge[0] == "NULL" or edge[1] == "NULL":
        #     print(edgeRow)
        #     print (row_counter)

        if not gr.has_node(edge[0]) :gr.add_node(edge[0])
        if not gr.has_node(edge[1]) :gr.add_node(edge[1])
        if not gr.has_edge(tuple(edge)) : gr.add_edge(tuple(edge))
        # outDegrees[edge[0]]+=1
        # inDegrees[edge[1]]+=1
        if row_counter >= LIMIT_NUM_ROWS:
            break


# inDegrees = pickle.load(open(os.path.join(output_dir, 'inDegreeDistributions.pickle'), 'rb'))
# outDegrees = pickle.load(open(os.path.join(output_dir, 'outDegreeDistributions.pickle'), 'rb'))

# inOutRatio = { k: inDegrees.get(k, 0) / outDegrees.get(k, 0) for k in set(inDegrees) | set(outDegrees) }

pickle.dump(gr, open(os.path.join(output_dir, 'citationGraph '+ str(row_counter)+'.pickle'), 'wb'))

print('')