__author__ = 'slouis'
# Reads the citation data (row by row) and creates dictionary of in/out degrees
# TODO: choose destination for output files

'''
This file reads in/out degree distributions of the citation graph.
The nodes are from both files: patent.txt & citations.txt files (to ensure we have also nodes of degree 0.

Outputs:
inDegreeDistributions <LIMIT_NUM_ROWS>.pickle - dictionary of in-degrees (key = patentID, val = inDegree)
outDegreeDistributions <LIMIT_NUM_ROWS>.pickle - dictionary of out-degrees (key = patentID, val = outDegree)
inDegreeDistributions <LIMIT_NUM_ROWS>.png - plot of the in-degree distribution
inDegreeDistributions <LIMIT_NUM_ROWS>.png - plot of the out-degree distribution
'''


from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import operator
try:
   import cPickle as pickle
except:
   import pickle
import os
from numpy import linspace as lrange



def plotDegreesFull(degreeDis, title = "degree distribution", ifShow = True, fileName = ""):
    print( Counter(degreeDis.values()).most_common(10))
    f, axarr = plt.subplots(3, sharex=False)

    # Plot rank-frequency
    l = list(map(list,zip(*sorted(degreeDis.items(), key=operator.itemgetter(1)))))
    axarr[0].plot(range(100,0,-1),l[1][1:101],'ro')
    axarr[0].set_xlabel('rank')
    axarr[0].set_ylabel('frequency')
    axarr[0].set_title(title + " - rank frequency")

    # Plot rank-frequency
    axarr[1].loglog(range(len(l[1]),0,-1),l[1],'ro')
    axarr[1].set_xlabel('log rank')
    axarr[1].set_ylabel('log frequency')
    axarr[1].set_title(title + " - rank frequency")

    # Plot histogram
    axarr[2].hist(list(degreeDis.values()))
    axarr[2].set_xlabel('degree')
    axarr[2].set_ylabel('frequency')
    axarr[2].set_title(title)


    # if ifShow : plt.show()
    if len(fileName): plt.savefig(fileName+'.png')

    plt.clf()

def plotDegrees(degrees, title = "degree distribution", ifShow = True, fileName = "", numOfBins = 100):
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


LIMIT_NUM_ROWS = float('Inf')

project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
# input_dir = os.path.join(project_dir, 'data', 'interim', 'sample')
# output_dir = os.path.join(project_dir, 'data', 'processed', 'sample')
input_dir = os.path.join(project_dir, 'data', 'raw')
output_dir = os.path.join(project_dir, 'data', 'processed', 'sample')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#Reading the files
print("Loading the data")
VERT_FILE_PATH = os.path.join(input_dir, 'patents.txt')
EDGE_FILE_PATH = os.path.join(input_dir, 'citations.txt')

inDegrees = defaultdict(int)
outDegrees = defaultdict(int)

print("Loading vertices")
with open(VERT_FILE_PATH, mode='r', encoding='utf-8') as vf:
    next(vf)
    row_counter = 0
    for line in vf:
        row_counter +=1
        inDegrees[line.strip().split()[0]]
        outDegrees[line.strip().split()[0]]
        if row_counter >= LIMIT_NUM_ROWS:
            break

print("reading edges")
with open(EDGE_FILE_PATH,  mode='r', encoding='utf-8') as ef:
    next(ef)
    row_counter = 0
    for edgeRow in ef:

        row_counter +=1
        edge = edgeRow.split()
        # if edge[0] == "NULL" or edge[1] == "NULL":
        #     print(edgeRow)
        #     print (row_counter)
        outDegrees[edge[0]]+=1
        inDegrees[edge[1]]+=1
        if row_counter >= LIMIT_NUM_ROWS:
            break
pickle.dump(inDegrees, open(os.path.join(output_dir, 'inDegreeDistributions '+ str(row_counter)+'.pickle'), 'wb'))
pickle.dump(outDegrees, open(os.path.join(output_dir, 'outDegreeDistributions '+ str(row_counter)+'.pickle'), 'wb'))

print('plotting indegree')
print("number of NULL vertices : "+ str(inDegrees.pop("NULL",0))+" . removed from plot.")

plotDegrees(inDegrees.values(), title = "In degree distribution", ifShow = False, fileName = os.path.join(output_dir, 'inDegreeDistributions '  + str(row_counter)), numOfBins=1000)
print('plotting outdegree')
print("number of NULL vertices : "+ str(outDegrees.pop("NULL",0))+" . removed from plot.")

plotDegrees(outDegrees.values(), title = "out degree distribution", ifShow = False, fileName = os.path.join(output_dir, 'outDegreeDistributions '  + str(row_counter)), numOfBins=1000)


print(outDegrees["NULL"])
print('Done')

