from sklearn.cluster import MiniBatchKMeans
import pandas as pd
from scipy.cluster.hierarchy import linkage
import warnings

"""
Build a dendogram of the patents, by creating basic level of k-means clusters and hierarchical clustering of
this clusters.
"""


def build_clusters(features_sparse_matrix, dendogram_df: pd.DataFrame, kmeans: int):
    """
    Build a dendogram of the patents
    :param features_sparse_matrix: scipy csr matrix of shape (m_patents, n_features)
    :param dendogram_df: the dataframe to populate with the results of the base clusters labels
    :param kmeans: num of clusters in the basis clustering level
    :return: the dendogram_df with the kmeans clusters labels and the Z matrix of the linkage process.
    """

    print("--Computing K-means")
    km = MiniBatchKMeans(n_clusters=kmeans, batch_size=(int(kmeans/2)))
    with warnings.catch_warnings(): # MiniBatchKMeans has a minor bug printing a warning. ignore this.
        warnings.simplefilter("ignore", category=DeprecationWarning)
        km.fit(features_sparse_matrix)
    dendogram_df.loc[:, 'kmeans_labels'] = km.labels_ # for each patent, save the base cluster.
    print('--Computing Hierarchical clustering ')
    z = linkage(km.cluster_centers_, method='average') # perform hierarchical clustering on top of the k clusters
    print("--Clustering done")

    return dendogram_df, z
