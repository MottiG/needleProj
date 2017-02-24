import pandas as pd
import os
from src.features.build_features import build_features
from src.models.build_dendogram import build_dendogram
from src.visualization import visualize
from sklearn.decomposition import TruncatedSVD
import time


def main():
    # for running on full data set SAMPLE = ""
    # SAMPLE = "sample"
    SAMPLE = "sample"

    # build dendogram
    treeLevels = [100, 7]  # number of clusters required for each level, must be descending order.
    N_COMPONENTS = 100

    # Load data
    project_dir = os.path.abspath(os.path.join(__file__, '..', '..'))
    input_dir = os.path.join(project_dir, 'data', 'processed',SAMPLE)
    output_dir = os.path.join(project_dir, 'data', 'processed','dendograms')
    if SAMPLE:
        output_filename = 'dendogram '+SAMPLE+' '+ '-'.join(str(x) for x in treeLevels) +'.pickle'
    else:
        output_filename = 'dendogram '+ '-'.join(str(x) for x in treeLevels) + '.pickle'

    print('Loading data')
    df = pd.read_pickle(os.path.join(input_dir, 'patent_table_clean.pickle'))

    # Create features
    features_sparse_matrix = build_features(df)

    # feature dimension reduction
    print("feature dimension reduction")
    pca = TruncatedSVD(n_components=N_COMPONENTS)
    t0 = time.time()
    features_sparse_matrix = pca.fit_transform(features_sparse_matrix)
    print ("    sparse pca to {} components --> running time : {} ".format(N_COMPONENTS, time.time() - t0))

    t0 = time.time()
    dendogram = build_dendogram(features_sparse_matrix, pd.DataFrame(index=df.index.copy()), treeLevels)
    print ("    dendogram building running time is: {} ".format(time.time() - t0))

    pd.to_pickle(dendogram, os.path.join(output_dir, output_filename))
    # visualize
    # visualize(dendogram)

if __name__ == '__main__':
    print('Lets go...')
    main()