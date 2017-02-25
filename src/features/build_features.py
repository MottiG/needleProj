from scipy import sparse
import numpy as np
import time
from .ft_idfer import TfIdfer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
# from .graph_features_builder import GraphFeaturesBuilder

"""
build all the features of the patents - text features (tfidf vectors) and graph features (communities)
"""

def build_features(df, cols_of_tfidf, n_components):
    """
    build all the features of the patents
    :param df: pandas DataFrame contains the patents data
    :param cols_of_tfidf: list of columns names to get tf-idf vectors for this columns
    :param n_components: number of components to save after dimension reducing of tfidf matrices
    :return: scipy csr matrix of shape (n_patents, n_features)
    """

    print('--Computing Tf-Idf features')
    t0 = time.time()
    tfIdfer = TfIdfer()
    tf_idf_features_dict = tfIdfer.get_features(df, cols_of_tfidf)
    print("--Tfidf total running time is: {} ".format(time.time() - t0))

    # feature dimension reduction
    print("--Feature dimension reduction")
    t0 = time.time()
    tfifd_features_sprs_matrix = sparse.hstack(list(tf_idf_features_dict.values()))
    del tf_idf_features_dict  # TODO check that its not reference!
    lsa = make_pipeline(TruncatedSVD(n_components), Normalizer(copy=False))
    tfifd_features_matrix = lsa.fit_transform(tfifd_features_sprs_matrix)
    print("--Dimension reduction total running time is: {} ".format(time.time() - t0))

    #print('Getting graph features')
    # t0 = time.time()
    # graph_geatures_Builder = GraphFeaturesBuilder()
    # graph_features = graph_geatures_Builder.get_features(N_COMMUNITIES_LIST)
    # print("Graph features total running time is: {} ".format(time.time() - t0))

    features_matrix = tfifd_features_matrix # np.hstack(list(tfifd_features_matrix))
    return features_matrix
