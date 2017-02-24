""" The package snap.py works on python 2.7 only """

from collections import Counter, defaultdict
import igraph

import matplotlib.pyplot as plt

# import snap

try:
   import cPickle as pickle
except:
   import pickle
import os
from numpy import linspace as lrange


'''
This file creates the dataframes from the txt files in /data/raw folder and saves them in /data/interim folder
'''

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

def patentID2nodeID(ptID):
    if ptID == "NULL": return 0
    letters2digits = {"" : "1", "D": "2", "H" : "3", "PP" : "4", "RE": "5", "T" : "6"}
    digits = ""
    letters = ""
    for s in ptID:
        if s.isdigit():
            if len(letters)==0 : return int(ptID)
            digits += s
        else:
            letters += s
    if letters in letters2digits:
        return int(letters2digits[letters] + digits)
    else:
        print(ptID)
        return "error"


def nodeID2patentID(nID):
    if nID == 0 : return "NULL"
    digits2letters = {"1" : "", "2": "D", "3" : "H", "4" : "PP", "5": "RE", "6": "T"}
    nID = str(nID)
    if len(nID) ==0 : return str(nID)
    return digits2letters[nID[0]] + nID[1:]

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
G = igraph.Graph.Read_Ncol(EDGE_FILE_PATH, directed=True)

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
    G.vs[range(vcount,vcount+len(vertices_set)-1)]["name"]=list(vertices_set)

## http://igraph.org/python/doc/tutorial/tutorial.html#igraph-and-the-outside-world
G.save(os.path.join(output_dir, 'citationGraph_'+ str(row_counter)+'.graph'), format="gml")