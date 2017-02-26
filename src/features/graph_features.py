"""

"""
import pandas as pd
import numpy
import time
import matplotlib.pyplot as plt
from scipy.sparse import lil_matrix as sparse_mat


try:
   import cPickle as pickle
except:
   import pickle
import os

class GraphFeatures:
    """
    Build tf-ifd features for a given dataframe
    """

    def __init__(self,df):

        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        graph_analysis_dir = os.path.join(project_dir, 'data', 'processed', 'citation graph')
        if not os.path.exists(graph_analysis_dir):
            os.makedirs(graph_analysis_dir)

        # Reading the files
        print("Loading the graph")
        self.G = pickle.load(open(os.path.join(graph_analysis_dir, 'citationGraph' + '.pickle'), 'rb'))
        self.G.simplify()
        try:
            self.G.delete_vertices(['citing','cited'])
        except:
            pass
        self.pt_index = df.index

        print("loading v_community_multilevel")
        self.v_community_multilevel = pickle.load(open(os.path.join(graph_analysis_dir, 'v_community_multilevel' + '.pickle'), 'rb'))
        print("loading v_community_label_propagation")
        self.v_community_label_propagation = pickle.load(open(os.path.join(graph_analysis_dir, 'v_community_label_propagation' + '.pickle'), 'rb'))

        print("dict:graphId2ptntID")
        self.graphId2ptntID = dict(zip(self.G.vs.indices, self.G.vs.get_attribute_values("name")))
        print("dict:ptntID2graphId")
        self.ptntID2graphId = dict(zip(self.G.vs.get_attribute_values("name"),self.G.vs.indices))
        print("dict:graphID2rowId")
        self.graphID2rowId = dict(zip([self.ptntID2graphId[self.pt_index[i]] for i in range(0,len(self.pt_index))],range(0,len(self.pt_index))))

    def community_vector_2sparse(self, v_community, minimal_community_size):

        com_sizes = [len(community) for community in v_community]
        num_of_large_communities = sum(i >= minimal_community_size for i in com_sizes)
        print("creating empty matrix")
        sparse_feature = sparse_mat((len(self.pt_index), num_of_large_communities + 1), dtype=bool)
        community_i = 0
        for community in v_community:
            if len(community) >= minimal_community_size:
                community_graphID2rowID = [self.graphID2rowId.get(x) for x in community if self.graphID2rowId.get(x) is not None]
                # community_graphID2rowID = [x for x in community_graphID2rowID if x is not None]
                # if num_of_large_communities % 500 == 0 :
                #     print("finished: " + str(community_i/num_of_large_communities))
                #
                sparse_feature[community_graphID2rowID, community_i] = True
                community_i += 1


        # print("reordering")
        # sparse_feature = sparse_mat((len(self.pt_index), num_of_large_communities + 1), dtype=bool)
        # for i in range(1,len(self.pt_index)):
        #     sparse_feature[i,:] = sparse_feature_graph_order[self.ptntID2graphId[self.pt_index[i]],:]

        return sparse_feature

    def get_features(self) -> dict:

        df_graph = pd.DataFrame( index = self.G.vs.get_attribute_values("name"))
        df_graph.loc[self.G.vs.get_attribute_values("name"), "graph_ids"] = self.G.vs.indices
        df_graph.loc[self.G.vs.get_attribute_values("name"), "ptids_ids"] = df_graph.index

        print("community_label_propagation")
        minimal_community_size = 3
        community_label_propagation_sparse = self.community_vector_2sparse(self.v_community_label_propagation,minimal_community_size)
        print("community_multilevel_sparse")
        num_of_levels = len(self.v_community_multilevel)
        community_multilevel_sparse = self.community_vector_2sparse(self.v_community_multilevel[num_of_levels-1],minimal_community_size)

        features_dict = dict()
        features_dict['community_label_propagation'] = community_label_propagation_sparse
        features_dict['community_multilevel'] = community_multilevel_sparse

        return features_dict

SAMPLE = 'sample'
print("Loading dataframe")
project_dir = os.path.abspath(os.path.join(__file__, '..', '..','..'))
input_dir = os.path.join(project_dir, 'data', 'processed',SAMPLE)
graph_analysis_dir = os.path.join(project_dir, 'data', 'processed','citation graph')
df = pd.read_pickle(os.path.join(input_dir, 'patent_table_clean_new.pickle'))

print("GraphFeatures")
test = GraphFeatures(df)

print("test.get_features()")
features_dict = test.get_features()

print("dump")
pickle.dump(features_dict , open(os.path.join(graph_analysis_dir, 'graph_features_dict'+'.pickle'),'wb'))

