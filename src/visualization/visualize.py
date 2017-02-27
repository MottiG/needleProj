import pandas as pd
import os
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
import pickle
from collections import Counter
import nltk


stops = nltk.corpus.stopwords.words('english') + \
['method','methods','apparatus','invention','system','device', 'thereof', 'one', 'present', 'least', 'also', 'may', 'wherein',
'use','used', 'useful', 'first', 'second', 'two', 'using', 'end']

project_dir = os.path.abspath(os.path.join( '__file__' , '..', '..'))
model_dir = os.path.join(project_dir, 'models')

# change this files to the most updated files we want to visualize
data = os.path.join(project_dir, 'data', 'processed', 'patent_table_clean_new.pickle')
model = os.path.join(model_dir, 'tf_idf_vectorizers.pickle')
kml = pd.read_pickle(os.path.join(model_dir, 'kmeans_labels639.pickle'))
with open(os.path.join(model_dir, 'z_matrix639.pickle'), 'rb') as f:
    z = pickle.load(f)
with open(model, 'rb') as f:
    mdl = pickle.load(f)['abstract']
df = pd.read_pickle(data)

def get_common_words(r: dendrogram, kml: pd.DataFrame):
    """
    get the most frequent words for a given dendrogram
    :param kml: a dataframe contains the cluster label for each patent
    :param r: a dendrogram of hierarchical clustering
    :return: dictionary with keys as boundaries of each cluster of the dendrogram and values as the
    most common word of the cluster in this boundaries.
    """

    dict_of_commons = {}
    bounds = [(118,418),(531,407),(148,219),(79,150),(134,384),(71,455),(58,226),(370,301),(477,173),
              (552,502),(32,380),(357,288),(29,154),(106,152),(231,331),(340,138),(65,634)]
    for bnd in bounds:
        print('\ncalculatin pair', bnd)
        cl = r['leaves'][r['leaves'].index(bnd[0]):r['leaves'].index(bnd[1])+1]
        ind = []
        for lcs in cl:
            ind += list(kml[kml['kmeans_labels']==lcs].index)
        txt = df.loc[ind]['abstract'].str.lower().str.replace(r'\|', ' ').str.cat(sep=' ')
        words = nltk.tokenize.word_tokenize(txt)
        words_dist = nltk.FreqDist(w for w in words if w not in stops and w.isalnum())
        dict_of_commons[bnd] = words_dist.most_common(100)
        print(list(zip(*words_dist.most_common(100)))[0])

    return dict_of_commons


def visualize_dendrogram(kmeans_labels_df, z_matrix):
    """
    visualize the dendrogram of the patents
    :param kmeans_labels_df: dataframe with the kmeans-label of each patent. the k clusters are the basis of the
    hierarchical clustering
    :param z_matrix: the matrix of hierarchical clusters
    :return:
    """
    plt.title('USA Patents Hierarchical Clustering Dendrogram')
    plt.figure(figsize=(120, 35))
    r = dendrogram(z, leaf_rotation=90., leaf_font_size=12.)
    plt.show()
    return r


