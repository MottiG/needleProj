from sklearn.cluster import KMeans
import pandas as pd

"""
Build a dendogram of the patents, by creating several levels of k-means clusters where each level has a
different number of clusters
"""

LEVELS = [100, 7]  # number of clusters required for each level, must be descending order.


def build_dendogram(features_sparse_matrix, dendogram_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a dendogram of the patents
    :param features_sparse_matrix: scipy csr matrix of shape (n_patents, n_features)
    :param dendogram_df: the dataframe to populate with the results of the clustering process
    :return: dataframe of shape (n_patents, n_levels_of_clusters) where each level has the cluster label for
    each patent
    """

    dendogram_df = pd.concat([dendogram_df, pd.DataFrame(columns=LEVELS)], copy=False)

    print("computing K-means...")
    last_centroids = None
    for i in range(len(LEVELS)):
        k = LEVELS[i]
        print("K-means for " + str(k) + " clusters")
        km = KMeans(n_clusters=k , n_jobs = -1)
        if i == 0:
            km.fit(features_sparse_matrix)
            dendogram_df.loc[:, k] = km.labels_
        else:
            km.fit(last_centroids)
            for j in range(len(last_centroids)):
                dendogram_df.ix[dendogram_df[LEVELS[i - 1]] == j, k] = km.labels_[j]
        last_centroids = km.cluster_centers_
    print("done.")

    return dendogram_df
