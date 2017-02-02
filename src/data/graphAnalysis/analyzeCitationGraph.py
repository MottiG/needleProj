""" The package snap.py works on python 2.7 only """

from collections import Counter, defaultdict

import matplotlib.pyplot as plt

import snap

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
    if letters2digits.has_key(letters):
        return int(letters2digits[letters] + digits)
    else:
        print ptID
        return "error"


def nodeID2patentID(nID):
    if nID == 0 : return "NULL"
    digits2letters = {"1" : "", "2": "D", "3" : "H", "4" : "PP", "5": "RE", "6": "T"}
    nID = str(nID)
    if len(nID) ==0 : return str(nID)
    return digits2letters[nID[0]] + nID[1:]

project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..','..'))
input_dir = os.path.join(project_dir, 'data', 'raw')
output_dir = os.path.join(project_dir, 'data', 'processed')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
citing_null = defaultdict(int)
cited_by_null = defaultdict(int)

#Reading the files
print("Loading the data")

edge_counter = 57584271 # 100000 or 57584271


cited_by_null = pickle.load(open(os.path.join(output_dir, 'cited_by_null_'+ str(edge_counter)+'.pickle'),'rb'))
FIn = snap.TFIn(os.path.join(output_dir, 'citationGraph_'+ str(edge_counter)+'.graph'))
gr = snap.TNGraph.Load(FIn)


# Clauset-Newman-Moore community detection method for large networks

CmtyV = snap.TCnComV()

print("converting to undirected")
gr = snap.ConvertGraph(snap.PUNGraph,gr)

print("Clauset-Newman-Moore community detection")
modularity = snap.CommunityCNM(gr, CmtyV)
print(len(CmtyV))

# for Cmty in CmtyV:
#     print "Community: "
#     for NI in Cmty:
#         print NI
print "The modularity of the network is %f" % modularity

print('')