from sklearn.cluster import KMeans
from src.features.ft_idfer import TfIdfer
from scipy.sparse import hstack


class ClusterModel:
    """
    perform initial clustering to the data
    """

    def __init__(self):
        self.vectorizer = TfIdfer()

    def get_labels(self, k, df, cols):
        """
        :param k: num of clusters
        :param df: the dataframe to analyze
        :param params: list contains the parameters we want to generate the clusters base on them
        :return: list of labels - label for each row of the df
        """
        km = KMeans(n_clusters=k)
        print("extract tf-idf on ", cols)
        features_dict = self.vectorizer.get_features(df=df, cols=cols)
        features_sparse_matrix = hstack(list(features_dict.values()))
        print("compute "+str(k)+" clusters")
        km.fit(features_sparse_matrix)
        return km.labels_





