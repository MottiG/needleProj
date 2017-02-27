import pandas as pd
import numpy
import random
import os

SAMPLE = "sample"
connected_patents_name = "all_connected_articles.pickle"
project_dir = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'processed', SAMPLE)

mild_connection_bound = 0.25
strong_connection_bound = 0.7

mild_connection_amount = 300
strong_connection_amount = 50



df = pd.read_pickle(os.path.join(input_dir, connected_patents_name))

mild_connected_patents = df[(df['percentage distance'] >= mild_connection_bound) &
                            (df['percentage distance'] < strong_connection_bound)]

strong_connected_patents = df[df['percentage distance'] >= strong_connection_bound]

mild_connected_patent_file = os.path.join(input_dir, 'mild_connected_patents')
strong_connected_patent_file = os.path.join(input_dir, 'strong_connected_patents')

mild_connected_patents = mild_connected_patents[:mild_connection_amount]
strong_connected_patents = strong_connected_patents[:strong_connection_amount]


pd.to_pickle(strong_connected_patents, strong_connected_patent_file)
pd.to_pickle(mild_connected_patents, mild_connected_patent_file)
