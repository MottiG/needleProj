__author__ = 'slouis'

from pygraph.classes.digraph import digraph
from pygraph.
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

gr = pickle.load(open(os.path.join(output_dir, 'citationGraph '+ str(10000)+'.pickle'), 'rb'))
# gr = digraph()
print(gr.nodes())
print(gr.edges())

feature = inDegree()