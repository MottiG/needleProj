from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt

def visualize_dendrogram(kmeans_labels_df, z_matrix):
    """
    visualize the dendrogram of the patents
    :param kmeans_labels_df:
    :param z_matrix:
    :return:
    """
    plt.title('USA Patents Hierarchical Clustering Dendrogram')
    dendrogram(z_matrix, leaf_rotation=90., leaf_font_size=8.)
    plt.show()
    plt.savefig('dendrogram.png')