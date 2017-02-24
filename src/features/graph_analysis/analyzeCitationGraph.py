__author__ = 'slouis'

from collections import Counter, defaultdict

import snap

try:
   import cPickle as pickle
except:
   import pickle
import os


"""
*** The package snap.py works on python 2.7 only  ***

This file reads in/out degree distributions of the citation graph.
The nodes are from both files: patent.txt & citations.txt files (to ensure we have also nodes of degree 0.

Outputs:
"""

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
        print (ptID)
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
edge_counter = 500000 # 100000 or 57584271

    #Load data
print("Loading the data")
cited_by_null = pickle.load(open(os.path.join(output_dir, 'cited_by_null_'+ str(edge_counter)+'.pickle'),'rb'))
FIn = snap.TFIn(os.path.join(output_dir, 'citationGraph_'+ str(edge_counter)+'.graph'))
gr = snap.TNGraph.Load(FIn)

# Clauset-Newman-Moore community detection method for large networks
print("Running Clauset-Newman-Moore community detection...")
CmtyV = snap.TCnComV()

print("converting to undirected")
gr = snap.ConvertGraph(snap.PUNGraph,gr)

print("Clauset-Newman-Moore community detection")
modularity = snap.CommunityCNM(gr, CmtyV)


print("Girvan-Newman community detection")
# modularity = snap.CommunityGirvanNewman(gr, CmtyV)


print("saving to file")

SOut = snap.TFOut(os.path.join(output_dir, 'communities_vec'+'.graph'))
CmtyV.Save(SOut)
SOut.Flush()

print ("The modularity of the network is %f" % modularity)
print ("Number of communities: %f" % len(CmtyV))


print('')