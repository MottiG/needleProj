import pandas as pd
import numpy, os, time

try:
   import cPickle as pickle
except:
   import pickle

print("Loading data")
project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..','..'))
input_dir = os.path.join(project_dir, 'data', 'processed')
graph_analysis_dir = os.path.join(project_dir, 'data', 'processed','citation graph')

G = pickle.load(open(os.path.join(graph_analysis_dir, 'citationGraph' + '.pickle'), 'rb'))

degree_dis = print(G.degree_distribution())

df = pd.read_pickle(os.path.join(input_dir, 'patent_table_clean.pickle'))


print("done!")