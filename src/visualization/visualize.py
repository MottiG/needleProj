from scipy.cluster.hierarchy import dendrogram, fcluster
import matplotlib.pyplot as plt

def visualize_dendrogram(kmeans_labels_df, z_matrix):
    """
    visualize the dendrogram of the patents
    :param kmeans_labels_df: dataframe with the kmeans-label of each patent. the k clusters are the basis of the
    hierarchical clustering
    :param z_matrix: the matrix of hierarchical clusters
    :return:
    """
    plt.title('USA Patents Hierarchical Clustering Dendrogram')
    dendrogram(z_matrix, leaf_rotation=90., leaf_font_size=8.)
    plt.show()
    plt.savefig('dendrogram.png')