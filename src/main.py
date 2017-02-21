import pandas as pd
import os
from features.build_features import build_features
from models.build_dendogram import build_dendogram
from visualization import visualize
from sklearn.decomposition import TruncatedSVD


def main():
    # Load data
    project_dir = os.path.abspath(os.path.join(__file__, '..', '..'))
    input_dir = os.path.join(project_dir, 'data', 'processed')
    print('Loading data')
    df = pd.read_pickle(os.path.join(input_dir, 'patent_table_clean.pickle'))

    # Create features
    features_sparse_matrix = build_features(df)

    # feature dimension reduction
    print("feature dimension reduction")
    pca = TruncatedSVD(n_components=100)
    features_sparse_matrix = pca.fit_transform(features_sparse_matrix)

    # build dendogram
    dendogram = build_dendogram(features_sparse_matrix, pd.DataFrame(index=df.index.copy()))
    pd.to_pickle(dendogram, os.path.join(input_dir, 'dendogram.pickle'))
    # visualize
    # visualize(dendogram)

if __name__ == '__main__':
    main()