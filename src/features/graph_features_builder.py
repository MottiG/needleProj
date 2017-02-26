"""

"""
from scipy.sparse import lil_matrix as sparse_mat
import pandas as pd

try:
   import cPickle as pickle
except:
   import pickle
import os


class GraphFeaturesBuilder:
    """
    Build tf-ifd features for a given dataframe
    """

    def __init__(self):
        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.graph_analysis_dir = os.path.join(project_dir, 'data', 'processed', 'citation graph')


        # Reading the files
        print("Loading the graph")
        self.G = pickle.load(open(os.path.join(self.graph_analysis_dir, 'citationGraph' + '.pickle'), 'rb'))
        self.G.simplify()
        try:
            self.G.delete_vertices(['citing','cited'])
        except:
            pass


        print("loading v_community_multilevel")
        self.v_community_multilevel = pickle.load(open(os.path.join(self.graph_analysis_dir, 'v_community_multilevel' + '.pickle'), 'rb'))
        print("loading v_community_label_propagation")
        self.v_community_label_propagation = pickle.load(open(os.path.join(self.graph_analysis_dir, 'v_community_label_propagation' + '.pickle'), 'rb'))

        self.graphId2ptntID = dict()
        self.ptntID2graphId = dict()
        self.graphID2rowId = dict()


    def community_vector_2sparse(self, v_community, minimal_community_size, pt_index):

        com_sizes = [len(community) for community in v_community]
        num_of_large_communities = sum(i >= minimal_community_size for i in com_sizes)

        print("creating empty matrix")
        sparse_feature = sparse_mat((len(pt_index), num_of_large_communities + 1), dtype=bool)

        community_i = 0
        for community in v_community:
            if len(community) >= minimal_community_size:
                community_graphID2rowID = [self.graphID2rowId.get(x) for x in community if self.graphID2rowId.get(x) is not None]
                sparse_feature[community_graphID2rowID, community_i] = True
                community_i += 1
        print("done.")

        return sparse_feature.tocsr()




    def get_features(self, df, minimal_community_size = 3) -> dict:

        print("dict:graphId2ptntID")
        self.graphId2ptntID = dict(zip(self.G.vs.indices, self.G.vs.get_attribute_values("name")))
        print("dict:ptntID2graphId")
        self.ptntID2graphId = dict(zip(self.G.vs.get_attribute_values("name"),self.G.vs.indices))
        print("dict:graphID2rowId")
        self.graphID2rowId = dict(zip([self.ptntID2graphId[self.pt_index[i]] for i in range(0,len(self.pt_index))],range(0,len(self.pt_index))))

        print("community_label_propagation")
        community_label_propagation_sparse = self.community_vector_2sparse(self.v_community_label_propagation,minimal_community_size, df.index)

        print("community_multilevel_sparse")
        num_of_levels = len(self.v_community_multilevel)
        community_multilevel_sparse = self.community_vector_2sparse(self.v_community_multilevel[num_of_levels-1],minimal_community_size, df.index)

        features_dict = dict()
        features_dict['community_label_propagation'] = community_label_propagation_sparse
        features_dict['community_multilevel'] = community_multilevel_sparse


        return features_dict



