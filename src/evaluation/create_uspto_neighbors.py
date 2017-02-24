
import pandas as pd
import numpy
import random
import os
from collections import deque, Counter
import matplotlib.pyplot as plt



SAMPLE = "sample"

project_dir = os.path.abspath(os.path.join(__file__, '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'processed', SAMPLE)
figure_dir = os.path.join(project_dir, 'reports', 'figures')
data_file = os.path.join(input_dir, 'patent_table_clean.pickle')
connected_articles_file = os.path.join(input_dir, 'all_connected_articles.pickle')
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
    dist = len(set(data_frame['class, mainclass'][ind1]).intersection(set(data_frame['class, mainclass'][ind2])))
    percentage_dist = 2*float(dist) / float(len(data_frame['class, mainclass'][ind1]) + len(data_frame['class, mainclass'][ind2]))
    return ((ind1, ind2), dist, percentage_dist)


columns = ['index1','index2', 'common class distance', 'percentage distance']
num_connected_articles = 1000
connected_articles = pd.DataFrame(index=numpy.arange(0, num_connected_articles), columns=columns)
curr_connected_ind = 0
num_random_pairs = 100000
distances = deque()
percentage_distances = deque()
for i in range(num_random_pairs):
    (ind1,ind2), dist, percentage_dist = select_random_pair(df)
    distances.append(dist)
    percentage_distances.append(percentage_dist)
    if (dist > 0):
        connected_articles.loc[curr_connected_ind] = [ind1, ind2, dist, percentage_dist]
        curr_connected_ind+=1

cnt = Counter(list(distances))
fig, ax = plt.subplots()
ax.bar(list(cnt.keys()), list(cnt.values()))
ax.set_yscale('log')
plt.savefig('distance_statistics.png')

fig, ax2 = plt.subplots()
n, bins, patches = plt.hist(list(percentage_distances), 5)
ax2.set_yscale('log')
plt.savefig('percentage_distance_statistic.png')

connected_articles = connected_articles[:curr_connected_ind+1]
pd.to_pickle(connected_articles, connected_articles_file)

