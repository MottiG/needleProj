import pandas as pd
import os
from src.features.build_features import build_features
from src.models.build_dendogram import build_dendogram
from src.visualization import visualize

# Load data
project_dir = os.path.abspath(os.path.join('__file__', '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'processed', 'sample')
df = pd.read_pickle(os.path.join(input_dir, 'patent_table_clean.pickle'))
dendogram_df = pd.DataFrame(index=df.index.copy())

# Create features
features_sparse_matrix = build_features(df)

# build dendogram
dendogram = build_dendogram(features_sparse_matrix, dendogram_df)

# visualize
# visualize(dendogram)

