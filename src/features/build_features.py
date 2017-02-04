"""

"""

import os
from scipy.sparse import hstack

from src.features.ft_idfer import TfIdfer
from src.features.graph_features_builder import GraphFeaturesBuilder

def build_features(df):
    # Load data
    project_dir = os.path.abspath(os.path.join( '__file__' , '..', '..','..'))
    input_dir = os.path.join(project_dir, 'data', 'processed', 'sample')

    tfIdfer = TfIdfer()
    cols = ['title', 'abstract']
    tf_idf_features_dict = tfIdfer.get_features(df, cols)

    graph_geatures_Builder = GraphFeaturesBuilder()
    n_cluster_list = [7,100,1000]
    graph_features_dict = graph_geatures_Builder.get_features(n_cluster_list)


    # features = hstack(features, format = "csr")
    # return features