import pandas as pd
import numpy
import random
import os
from collections import deque, Counter
import matplotlib.pyplot as plt


def extract_titles_abstracts(ind1, ind2):
    patent1 = df.loc[ind1]
    patent2 = df.loc[ind2]
    return patent1['title'], patent1['abstract'],patent2['title'],  patent2['abstract']

SAMPLE = ""

project_dir = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'processed', SAMPLE)
figure_dir = os.path.join(project_dir, 'reports', 'figures')
data_file = os.path.join(input_dir, 'patent_table_clean_new.pickle')
df = pd.read_pickle(data_file)


unconnected_articles = pd.read_pickle(os.path.join(input_dir, 'unconnected_patents_for_manual.pickle'))
topclass_neighbors = pd.read_pickle(os.path.join(input_dir, 'topclass_neighbors_for_manual.pickle'))
subclass_neighbors = pd.read_pickle(os.path.join(input_dir, 'subclass_neighbors_for_manual.pickle'))

full_table = pd.concat([unconnected_articles, topclass_neighbors, subclass_neighbors])
full_table = full_table.sample(frac=1).reset_index(drop=True)

full_table['p1_title'],  full_table['p1_abstract'],full_table['p2_title'],full_table['p2_abstract'] = \
    zip(*full_table.apply(lambda x: extract_titles_abstracts(x['ind1'], x['ind2']), axis=1))

full_table.to_csv(os.path.join(input_dir, 'evaluation_table.csv'))


