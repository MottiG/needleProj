from sklearn.cluster import KMeans
import pandas as pd
from scipy.cluster.hierarchy import linkage

"""
Build a dendogram of the patents, by creating several levels of k-means clusters where each level has a
different number of clusters
"""


def build_clusters(features_sparse_matrix, dendogram_df: pd.DataFrame, tree_levels : list):
    """
    Build a dendogram of the patents
    :param features_sparse_matrix: scipy csr matrix of shape (n_patents, n_features)
    :param dendogram_df: the dataframe to populate with the results of the clustering process
    :return: dataframe of shape (n_patents, n_levels_of_clusters) where each level has the cluster label for
    each patent
    """

    # For now the function returns the dendogram_df with only the kmeans clusters labels and in addition the
    # Z matrix of the linkage process.

    # dendogram_df = pd.concat([dendogram_df, pd.DataFrame(columns=tree_levels)], copy=False)

    print("--Computing K-means")
    # last_centroids = None
    # for i in range(len(tree_levels)):
    #     k = tree_levels[i]
    #     print("----K-means for " + str(k) + " clusters")
    #     km = KMeans(n_clusters=k, n_jobs=-1)
    #     if i == 0:
    #         km.fit(features_sparse_matrix)
    #         dendogram_df.loc[:, k] = km.labels_
    #     else:
    #         km.fit(last_centroids)
    #         for j in range(len(last_centroids)):
    #             dendogram_df.loc[dendogram_df[tree_levels[i - 1]] == j, k] = km.labels_[j]
    #     last_centroids = km.cluster_centers_

    km = KMeans(n_clusters=200, n_jobs=-1)
    km.fit(features_sparse_matrix)
    dendogram_df.loc[:, 'kmeans_labels'] = km.labels_
    print('--Computing Hierarchical clustering ')
    z = linkage(km.cluster_centers_, method='average')
    print("--Clustering done")

    return dendogram_df, z
