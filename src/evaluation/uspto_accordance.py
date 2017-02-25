import pandas as pd
import numpy
import random
import os
from collections import deque, Counter
import matplotlib.pyplot as plt

def are_topclass_neighbors(ind1, ind2, dendrogram, top_class_label):
    if ind1 in dendrogram.index and ind2 in dendrogram.index:
        return float(dendrogram.loc[ind1][top_class_label] == dendrogram.loc[ind2][top_class_label])
    else:
        return None

def are_unconnected(ind1, ind2, dendrogram, top_class_label):
    return float(dendrogram.loc[ind1][top_class_label] == dendrogram.loc[ind2][top_class_label])


def evaluate(dendrogram, input_dir, top_class_label):

    unconnected_articles = pd.read_pickle(os.path.join(input_dir, 'unconnected_patents.pickle'))
    topclass_neighbors = pd.read_pickle(os.path.join(input_dir, 'topclass_neighbors.pickle'))
    subclass_neighbors = pd.read_pickle(os.path.join(input_dir, 'subclass_neighbors.pickle'))

    result_topclass = topclass_neighbors.apply(lambda x: are_topclass_neighbors(x['ind1'], x['ind2'], dendrogram,top_class_label ), axis=1)
    topclass_grade = result_topclass.sum() / len(result_topclass)
    return topclass_grade


