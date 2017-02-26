"""

"""

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
        graph_analysis_dir = os.path.join(project_dir, 'data', 'processed', 'citation graph')

        # Reading the files
        print("Loading the graph features")
        self.features_dict= pickle.load(open(os.path.join(graph_analysis_dir, 'graph_features_dict' + '.pickle'), 'rb'))


    def get_features(self) -> dict:
        return self.features_dict


