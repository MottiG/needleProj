
import pandas as pd
import numpy
import random
import os
from collections import deque, Counter
import matplotlib.pyplot as plt


SAMPLE = "sample"

project_dir = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'processed', SAMPLE)
figure_dir = os.path.join(project_dir, 'reports', 'figures')
data_file = os.path.join(input_dir, 'patent_table_clean_10k.pickle')
connected_articles_file = os.path.join(input_dir, 'all_connected_patents.pickle')
df = pd.read_pickle(data_file)


# In[47]:

def select_random_pair(data_frame):
    while True:
        int_ind1 = random.randint(0,len(data_frame)-1)
        int_ind2 = random.randint(0,len(data_frame)-1)
        if (int_ind1 != int_ind2):
            break

    ind1 = data_frame.index[int_ind1]
    ind2 = data_frame.index[int_ind2]
    return ind1, ind2


# def create_unconnected_articles(df, num_articles):
#     columns = ['index1','index2']
#     unconnected_articles = pd.DataFrame(index=numpy.arange(0, num_articles), columns=columns)
#     curr_ind = 0
#     while curr_ind < num_articles:
#         (ind1,ind2), dist, percentage_dist = select_random_pair(df)
#         if (dist == 0):
#             unconnected_articles.loc[curr_ind] = [ind1, ind2]
#             curr_ind += 1
#     return unconnected_articles
#
#
# def create_connected_articles(df, num_random_pairs, savefig=False):
#     columns = ['index1','index2', 'common class distance', 'percentage distance']
#     num_connected_articles = num_random_pairs/1000
#     connected_articles = pd.DataFrame(index=numpy.arange(0, num_connected_articles), columns=columns)
#     curr_connected_ind = 0
#     distances = deque()
#     percentage_distances = deque()
#     for i in range(num_random_pairs):
#         (ind1,ind2), dist, percentage_dist = select_random_pair(df)
#         distances.append(dist)
#         percentage_distances.append(percentage_dist)
#         if (dist > 0):
#             if curr_connected_ind < num_connected_articles:
#                 connected_articles.loc[curr_connected_ind] = [ind1, ind2, dist, percentage_dist]
#                 curr_connected_ind+=1
#
#     if savefig:
#         cnt = Counter(list(distances))
#         fig, ax = plt.subplots()
#         ax.bar(list(cnt.keys()), list(cnt.values()))
#         ax.set_yscale('log')
#         plt.savefig(os.path.join(figure_dir, 'distance_statistics.png'))
#
#     if savefig:
#         fig, ax2 = plt.subplots()
#         n, bins, patches = plt.hist(list(percentage_distances), 10)
#         ax2.set_yscale('log')
#         plt.savefig(os.path.join(figure_dir, 'percentage_distance_statistic.png'))
#
#     connected_articles = connected_articles[:curr_connected_ind+1]
#     return connected_articles

columns = ['ind1', 'ind2']
num_unconnected_patents = 10000
num_topclass_neighbors = 1000
num_subclass_neighbors = 300

unconnected_patents = pd.DataFrame(index= numpy.arange(0, num_unconnected_patents), columns=columns)
topclass_neighbors = pd.DataFrame(index= numpy.arange(0, num_topclass_neighbors), columns=columns)
subclass_neighbors = pd.DataFrame(index= numpy.arange(0, num_subclass_neighbors), columns=columns)

curr_unconnected = 0
curr_topclass = 0
curr_subclass = 0
num_pairs = 0

while (curr_unconnected < num_unconnected_patents and
       curr_topclass < num_topclass_neighbors and
       curr_subclass < num_subclass_neighbors):
    ind1, ind2 = select_random_pair(df)
    pat1 = df.loc[ind1]
    pat2 = df.loc[ind2]
    if (pat1['main top class'] == pat2['main top class']):
        if pat1['main subclass'] == pat2['main subclass']:
            if (curr_topclass < num_topclass_neighbors):
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
unconnected_articles_file = os.path.join(input_dir, 'unconnected_patents.pickle')
topclass_neighbors_file = os.path.join(input_dir, 'topclass_neighbors.pickle')
subclass_neighbors_file = os.path.join(input_dir, 'subclass_neighbors.pickle')

pd.to_pickle(unconnected_patents, unconnected_articles_file)
pd.to_pickle(subclass_neighbors, subclass_neighbors_file)
pd.to_pickle(topclass_neighbors, topclass_neighbors_file)