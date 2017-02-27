from sklearn.cluster import MiniBatchKMeans
import pandas as pd
from scipy.cluster.hierarchy import linkage
import warnings

"""
Build a dendogram of the patents, by creating several levels of k-means clusters where each level has a
different number of clusters
"""


def build_clusters(features_sparse_matrix, dendogram_df: pd.DataFrame, kmeans: int):
    """
    Build a dendogram of the patents
    :param features_sparse_matrix: scipy csr matrix of shape (n_patents, n_features)
    :param dendogram_df: the dataframe to populate with the results of the clustering process
    :param kmeans: num of clusters in the basis clustering level
    :return: the dendogram_df with the kmeans clusters labels and the Z matrix of the linkage process.
    """

    print("--Computing K-means")
    km = MiniBatchKMeans(n_clusters=kmeans, batch_size=(int(kmeans/2)))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        km.fit(features_sparse_matrix)
    dendogram_df.loc[:, 'kmeans_labels'] = km.labels_
    print('--Computing Hierarchical clustering ')
    z = linkage(km.cluster_centers_, method='average')
    print("--Clustering done")

    return dendogram_df, z
