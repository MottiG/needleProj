import pandas as pd
import os
from src.features.build_features import build_features
from src.models.build_dendogram import build_dendogram
from src.visualization import visualize

# Load data
project_dir = os.path.abspath(os.path.join('__file__', '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'processed')
print('Loading data')
df = pd.read_pickle(os.path.join(input_dir, 'patent_table_clean.pickle'))

# Create features
features_sparse_matrix = build_features(df)

# build dendogram
dendogram = build_dendogram(features_sparse_matrix, pd.DataFrame(index=df.index.copy()))
pd.to_pickle(dendogram, os.path.join(input_dir, 'dendogram.pickle'))
# visualize
# visualize(dendogram)

