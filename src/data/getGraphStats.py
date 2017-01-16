__author__ = 'slouis'

import random
import os
from collections import defaultdict, Counter

os.chdir(os.path.dirname(os.getcwd()))
os.chdir(os.path.dirname(os.getcwd()))

PERCENTS = 0.15   # percents of nodes in the sample
VERT_FILE = os.path.join(os.getcwd(), 'data', 'raw','patents.txt')
EDGE_FILE = os.path.join(os.getcwd(), 'data', 'raw','citations.txt')

inDegrees = defaultdict(int)
outDegrees = defaultdict(int)

print("Getting vertices")
with open(VERT_FILE) as vf:
    next(vf)
    for line in vf:
        inDegrees[line.strip().split()[0]]
        outDegrees[line.strip().split()[0]]

print("Getting out degree")
with open(EDGE_FILE,  mode='rb') as ef:
    next(ef)
    for edgeRow in ef:
        edge = edgeRow.split()
        outDegrees[edge[0]]+=1
        inDegrees[edge[1]]+=1

print( "in-degrees distribution")
print( Counter(inDegrees.values()).most_common())

print( "in-degrees distribution")
print( Counter(outDegrees.values()).most_common())

print('Done')
