from scipy.sparse import lil_matrix as sparse_mat

try:
   import cPickle as pickle
except:
   import pickle
import os


class GraphFeaturesBuilder:
    """
    Build graph features for a given dataframe
    """

    def __init__(self):
        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.graph_analysis_dir = os.path.join(project_dir, 'data', 'processed', 'citation graph')

        # Reading the graph
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

        # Initialization of dictionary mapping the row index, the patent ID (string) and the node IDs (in the graph)
        self.graphID2ptntID = dict()
        self.ptntID2graphID = dict()
        self.graphID2rowID = dict()


    def community_vector_2sparse(self, v_community, minimal_community_size, pt_index):
        """
        for a given community vector data
        :param v_community: vertex communities as igraph.VertexClustering object, equivalent to list of lists ov vectors.
        :param minimal_community_size: communities bellow this integer will be omitted.
        :return: scipy.sparse.csr object, sparse matrix for community.
        """

        com_sizes = [len(community) for community in v_community]   # list of community sizes
        num_of_large_communities = sum(i >= minimal_community_size for i in com_sizes)  # count "large" communities

        print("creating empty matrix")
        sparse_feature = sparse_mat((len(pt_index), num_of_large_communities + 1), dtype=bool)

        print("community list to sparse matrix...")
        community_i = 0
        for community in v_community:
            if len(community) >= minimal_community_size:
                community_graphID2rowID = [self.graphID2rowID.get(x) for x in community if self.graphID2rowID.get(x) is not None]
                sparse_feature[community_graphID2rowID, community_i] = True
                community_i += 1
        print("done.")

        return sparse_feature.tocsr()




    def get_features(self, df, minimal_community_size = 3) -> dict:
        """
        for a given dataframe, create sparse matrices representing communities (dummy variable for each community).
        :param df: pandas dataframe contains the patents data
        :param minimal_community_size: communities bellow this integer will be omitted. default 3.
        :return: dictionary with keys name of communit-detection-algorithms used and values sparse matrix for community.
        """

        print("dict:graphID2ptntID")
        self.graphID2ptntID = dict(zip(self.G.vs.indices, self.G.vs.get_attribute_values("name")))
        print("dict:ptntID2graphID")
        self.ptntID2graphID = dict(zip(self.G.vs.get_attribute_values("name"),self.G.vs.indices))
        print("dict:graphID2rowID")
        self.graphID2rowID = dict(zip([self.ptntID2graphID[df.index[i]] for i in range(0,len(df.index))],range(0,len(df.index))))

        print("community_label_propagation")
        community_label_propagation_sparse = self.community_vector_2sparse(self.v_community_label_propagation,minimal_community_size, df.index)

        print("community_multilevel_sparse")
        num_of_levels = len(self.v_community_multilevel)
        community_multilevel_sparse = self.community_vector_2sparse(self.v_community_multilevel[num_of_levels-1],minimal_community_size, df.index)

        features_dict = dict()
        features_dict['community_label_propagation'] = community_label_propagation_sparse
        features_dict['community_multilevel'] = community_multilevel_sparse


        return features_dict



