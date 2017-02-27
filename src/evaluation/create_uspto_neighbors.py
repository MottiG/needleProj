
import pandas as pd
import numpy
import random
import os
from collections import deque, Counter
import matplotlib.pyplot as plt


SAMPLE = ""

project_dir = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'processed', SAMPLE)
figure_dir = os.path.join(project_dir, 'reports', 'figures')
data_file = os.path.join(input_dir, 'patent_table_clean_new_no_abstract.pickle')
connected_articles_file = os.path.join(input_dir, 'all_connected_patents.pickle')
df = pd.read_pickle(data_file)


def select_random_pair(data_frame):
    while True:
        int_ind1 = random.randint(0,len(data_frame)-1)
        int_ind2 = random.randint(0,len(data_frame)-1)
        if (int_ind1 != int_ind2):
            break

    ind1 = data_frame.index[int_ind1]
    ind2 = data_frame.index[int_ind2]
    return ind1, ind2



columns = ['ind1', 'ind2']
num_unconnected_patents = 150
num_topclass_neighbors = 30
num_subclass_neighbors = 20

unconnected_patents = pd.DataFrame(index= numpy.arange(0, num_unconnected_patents), columns=columns)
topclass_neighbors = pd.DataFrame(index= numpy.arange(0, num_topclass_neighbors), columns=columns)
subclass_neighbors = pd.DataFrame(index= numpy.arange(0, num_subclass_neighbors), columns=columns)

curr_unconnected = 0
curr_topclass = 0
curr_subclass = 0
num_pairs = 0

while (curr_unconnected < num_unconnected_patents or
       curr_topclass < num_topclass_neighbors or
       curr_subclass < num_subclass_neighbors):
    ind1, ind2 = select_random_pair(df)
    pat1 = df.loc[ind1]
    pat2 = df.loc[ind2]
    if (pat1['main top class'] == pat2['main top class']):
        if pat1['main subclass'] == pat2['main subclass']:
            if (curr_subclass < num_subclass_neighbors):
                subclass_neighbors.loc[curr_subclass] = [ind1, ind2]
                curr_subclass += 1
        else:
            if (curr_topclass < num_topclass_neighbors):
                topclass_neighbors.loc[curr_topclass] = [ind1, ind2]
                curr_topclass += 1
    else:
        if curr_unconnected < num_unconnected_patents:
            unconnected_patents.loc[curr_unconnected] = [ind1, ind2]
            curr_unconnected +=1

    num_pairs +=1

print(str(num_pairs) + ' iterations')
unconnected_articles_file = os.path.join(input_dir, 'unconnected_patents_for_manual.pickle')
topclass_neighbors_file = os.path.join(input_dir, 'topclass_neighbors_for_manual.pickle')
subclass_neighbors_file = os.path.join(input_dir, 'subclass_neighbors_for_manual.pickle')

pd.to_pickle(unconnected_patents, unconnected_articles_file)
pd.to_pickle(subclass_neighbors, subclass_neighbors_file)
pd.to_pickle(topclass_neighbors, topclass_neighbors_file)