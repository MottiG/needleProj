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

try:
   import cPickle as pickle
except:
   import pickle
import os

project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
input_dir = os.path.join(project_dir, 'reports', 'descriptive stats')
output_dir = os.path.join(project_dir, 'data', 'processed', 'sample')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


inDegrees = pickle.load(open(os.path.join(output_dir, 'inDegreeDistributions.pickle'), 'rb'))
outDegrees = pickle.load(open(os.path.join(output_dir, 'outDegreeDistributions.pickle'), 'rb'))

inOutRatio = { k: x.get(k, 0) / y.get(k, 0) for k in set(x) | set(y) }