import pandas as pd
import os
import time

from src.features.build_features import build_features
from src.models.build_dendogram import build_dendogram
from src.visualization import visualize
from src.evaluation.uspto_accordance import evaluate


def main():
    # for running on full data set SAMPLE = ""
    SAMPLE = "sample"

    # features parameters
    cols_of_tfidf = ['title', 'abstract']  # name of columns to apply tfidf vectorization
    n_components = 100  # number of components to save after dimension reducing of tfidf matrices

    # dendogram parameters
    tree_levels = [20, 7]  # number of clusters required for each level, must be descending order.

    # Load data
    project_dir = os.path.abspath(os.path.join(__file__, '..', '..'))
    input_dir = os.path.join(project_dir, 'data', 'processed', SAMPLE)
    output_dir = os.path.join(project_dir, 'data', 'processed', 'dendograms')
    if SAMPLE:
        output_filename = 'dendogram '+SAMPLE+' '+'-'.join(str(x) for x in tree_levels)+'.pickle'
    else:
        output_filename = 'dendogram '+'-'.join(str(x) for x in tree_levels)+'.pickle'

    print('Loading data')
    df = pd.read_pickle(os.path.join(input_dir, 'patent_table_clean.pickle'))

    # Create features
    features_matrix = build_features(df, cols_of_tfidf, n_components)

    t0 = time.time()
    dendogram = build_dendogram(features_matrix, pd.DataFrame(index=df.index.copy()), tree_levels)
    print ("    dendogram building running time is: {} ".format(time.time() - t0))

    pd.to_pickle(dendogram, os.path.join(output_dir, output_filename))

    #TODO automate
    top_class_label = 20
    top_class_grade = evaluate(dendogram, input_dir, top_class_label)
    print('Top class neighborhood grade: ' +  str(top_class_grade))

    # visualize
    # visualize(dendogram)

if __name__ == '__main__':
    print('Lets go...')
    main()