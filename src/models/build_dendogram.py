"""

"""

from sklearn.cluster import KMeans, MiniBatchKMeans
import time


def build_dendogram(features_sparse_matrix):
    print("K-means...")
    for k in [7,30,100]:
        print("K-means for " + str(k) + " clusters")
        t0 = time.time()
        km = KMeans(n_clusters=k)
        km.fit(features)
        km_labels = km.labels_
        t_batch = time.time() - t0

        print("MiniBatchKMeans for " + str(k) + " clusters")
        t0 = time.time()
        km = MiniBatchKMeans(n_clusters=k)
        km.fit(features)
        mbk_labels = km.labels_
        t_mini_batch = time.time() - t0
    print("done.")

    return dendogram