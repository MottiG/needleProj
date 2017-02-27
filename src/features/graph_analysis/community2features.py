from collections import Counter, defaultdict
import igraph

import matplotlib.pyplot as plt

try:
   import cPickle as pickle
except:
   import pickle
import os
from numpy import linspace as lrange

__author__ = 'slouis'
'''
This file runs community detection algorithms on the citation graph
Note that (most) of the algorithms require UNDIRECTED graph

Outputs:
v_community_multilevel: a list of VertexClustering (igraph) objects, one corresponding to each level.
v_community_fastgreedy : an appropriate VertexDendrogram (igraph) object.
'''



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

project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..','..'))
graph_analysis_dir = os.path.join(project_dir, 'data', 'processed','citation graph')
if not os.path.exists(graph_analysis_dir):
    os.makedirs(graph_analysis_dir)
citing_null = defaultdict(int)
cited_by_null = defaultdict(int)

#Reading the files
print("Loading the graph")
# G = igraph.Graph.Read_GML(os.path.join(graph_analysis_dir, 'citationGraph'+'.graph'))
# G = pickle.dump(open(os.path.join(graph_analysis_dir, 'citationGraph'+'.pickle'),'wb'))
G = pickle.load(open(os.path.join(graph_analysis_dir, 'citationGraph'+'.pickle'),'rb'))
G.simplify()

print("v_community_multilevel")
v_community_multilevel = G.community_multilevel(return_levels = True)

# print("v_community_fastgreedy")
# v_community_fastgreedy = G.community_fastgreedy()

print("saving to files")
pickle.dump(v_community_multilevel, open(os.path.join(graph_analysis_dir, 'v_community_multilevel'+'.pickle'),'wb'))
# pickle.dump(v_community_fastgreedy, open(os.path.join(graph_analysis_dir, 'v_community_fastgreedy'+'.pickle'),'wb'))

print("Done!")
