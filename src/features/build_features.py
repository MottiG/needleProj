import os
from scipy.sparse import hstack
from src.features.ft_idfer import TfIdfer
from src.features.graph_features_builder import GraphFeaturesBuilder

"""
build all the features of the patents - text features (tfidf vectors) and graph features (communities)
"""

COLS = ['title', 'abstract']  # name of columns to apply tfidf vectorization
N_COMMUNITIES_LIST = [7, 100, 1000]  # number of communities to find in the graph of patents


def build_features(df):
    """
    build all the features of the patents
    :param df: pandas DataFrame contains the patents data
    :return: scipy csr matrix of shape (n_patents, n_features)
    """

    # project_dir = os.path.abspath(os.path.join( '__file__' , '..', '..','..'))
    # input_dir = os.path.join(project_dir, 'data', 'processed', 'sample')

    tfIdfer = TfIdfer()
    tf_idf_features_dict = tfIdfer.get_features(df, COLS)

    graph_geatures_Builder = GraphFeaturesBuilder()
    # graph_features_dict = graph_geatures_Builder.get_features(N_COMMUNITIES_LIST)

    features_sparse_matrix = hstack(list(tf_idf_features_dict.values()))
    return features_sparse_matrix
