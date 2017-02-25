import pandas as pd
import os
from src.features.build_features import build_features
from src.models.build_dendogram import build_dendogram
from src.visualization import visualize
import time


def main():
    # for running on full data set SAMPLE = ""
    SAMPLE = "sample"
    sample_file_name = 'patent_table_clean_10k'

    # features parameters
    cols_of_tfidf = ['title', 'abstract']  # name of columns to apply tfidf vectorization
    n_components = 100  # number of components to save after dimension reducing of tfidf matrices

    # dendogram parameters
    tree_levels = [100, 8]  # number of clusters required for each level, must be descending order.

    # Load data
    project_dir = os.path.abspath(os.path.join(__file__, '..', '..'))
    input_dir = os.path.join(project_dir, 'data', 'processed', SAMPLE)
    output_dir = os.path.join(project_dir, 'data', 'processed', 'dendograms')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if SAMPLE:
        output_filename = 'dendogram '+sample_file_name+' '+'-'.join(str(x) for x in tree_levels)+'.pickle'
    else:
        output_filename = 'dendogram '+'-'.join(str(x) for x in tree_levels)+'.pickle'

    print('Loading data')
    df = pd.read_pickle(os.path.join(input_dir, sample_file_name+'.pickle'))

    # Create features
    t0 = time.time()
    print('Building features')
    features_matrix = build_features(df, cols_of_tfidf, n_components)
    print("Features building total running time is: {} ".format(time.time() - t0))

    print('Building dendogram')
    t0 = time.time()
    dendogram = build_dendogram(features_matrix, pd.DataFrame(index=df.index.copy()), tree_levels)
    print ("Dendogram building running time is: {} ".format(time.time() - t0))

    print('Saving output as', output_filename)
    pd.to_pickle(dendogram, os.path.join(output_dir, output_filename))
    # visualize
    # visualize(dendogram)

if __name__ == '__main__':

    print('Yallah Balagan...')
    main()