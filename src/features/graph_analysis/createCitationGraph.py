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
VERT_FILE_PATH = os.path.join(input_dir, 'patents.txt')
EDGE_FILE_PATH = os.path.join(input_dir, 'citations.txt')

LIMIT_NUM_ROWS = 100000 #float("inf") #

if LIMIT_NUM_ROWS < float("inf"):
    gr = snap.TNGraph.New(LIMIT_NUM_ROWS, 3*LIMIT_NUM_ROWS) # New(Nodes, Edges)
else:
    gr = snap.TNGraph.New(int(3e6),int(60e6))


print("Loading vertices")
with open(VERT_FILE_PATH, mode='r') as vf:
    next(vf)
    row_counter = 0
    for line in vf:
        if row_counter % 100000 == 0 : print(row_counter)
        row_counter +=1
        patentId = patentID2nodeID(line.strip().split()[0])

        if not gr.IsNode(patentId):
            nodeI = gr.AddNode(patentId)
        if row_counter >= LIMIT_NUM_ROWS:
            break

print("reading edges")
with open(EDGE_FILE_PATH,  mode='r') as ef:
    next(ef)
    row_counter = 0
    for edgeRow in ef:
        if row_counter % 100000 == 0 : print(row_counter)
        row_counter +=1
        edge = edgeRow.split()
        # if edge[0] == "NULL" or edge[1] == "NULL":
        #     print(edgeRow)
        #     print (row_counter)

        p0 = patentID2nodeID(edge[0])
        p1 = patentID2nodeID(edge[1])
        if not gr.IsNode(p0) :gr.AddNode(p0)
        if not gr.IsNode(p1) :gr.AddNode(p1)
        if p0 and p1 :
            gr.AddEdge(p0,p1)
        else:
            if p0 : # p0 is citing null  (p0-->null)  REDUNDANT : NEVER HAPPENS IN OUR DATA!
                citing_null[p0] += 1
            else:   # p1 is cited by null  (null-->p1)
                cited_by_null[p1] += 1
        # outDegrees[edge[0]]+=1
        # inDegrees[edge[1]]+=1
        if row_counter >= LIMIT_NUM_ROWS:
            break


# inDegrees = pickle.load(open(os.path.join(output_dir, 'inDegreeDistributions.pickle'), 'rb'))
# outDegrees = pickle.load(open(os.path.join(output_dir, 'outDegreeDistributions.pickle'), 'rb'))

# inOutRatio = { k: inDegrees.get(k, 0) / outDegrees.get(k, 0) for k in set(inDegrees) | set(outDegrees) }

pickle.dump(cited_by_null,open(os.path.join(output_dir, 'cited_by_null_'+ str(row_counter)+'.pickle'),'wb'))
FOut = snap.TFOut(os.path.join(output_dir, 'citationGraph_'+ str(row_counter)+'.graph'))
gr.Save(FOut)
FOut.Flush()

print('')