import pandas as pd
import os
from features.build_features import build_features
from models.build_clusters import build_clusters
import pickle
from visualization.visualize import visualize_dendrogram
import time


def main():
    # for running on full data set SAMPLE = ""
    SAMPLE = "sample"
    sample_file_name = 'patent_table_new_50k'

    # features parameters
    cols_of_tfidf = ['abstract']  # name of columns to apply tfidf vectorization
    n_components = 100  # number of components to save after dimension reducing of tfidf matrices

    # dendogram parameters TODO not in use
    tree_levels = [100, 8]  # number of clusters required for each level, must be descending order.

    # Load data
    project_dir = os.path.abspath(os.path.join(__file__, '..', '..'))
    input_dir = os.path.join(project_dir, 'data', 'processed', SAMPLE)
    output_dir = os.path.join(project_dir, 'data', 'processed', 'dendograms')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if SAMPLE:
        kmeans_labels_filename = 'kmeans_labels '+sample_file_name+'.pickle'
        z_matrix_filename = 'z_matrix '+sample_file_name+'.pickle'
    else:
        kmeans_labels_filename = 'kmeans_labels.pickle'
        z_matrix_filename = 'z_matrix.pickle'

    print('Loading data')
    df = pd.read_pickle(os.path.join(input_dir, sample_file_name+'.pickle'))

    # Create features
    t0 = time.time()
    print('Building features')
    features_matrix = build_features(df, cols_of_tfidf, n_components)
    print("Features building total running time is: {} ".format(time.time() - t0))

    print('Building clusters')
    t0 = time.time()
    kmeans_labels, z_matrix = build_clusters(features_matrix, pd.DataFrame(index=df.index.copy()), tree_levels)
    print ("Clusters building running time is: {} ".format(time.time() - t0))

    print('Saving kmeans labels as', kmeans_labels_filename)
    pd.to_pickle(kmeans_labels, os.path.join(output_dir, kmeans_labels_filename))
    print('Saving z matrix as', z_matrix_filename)
    with open(os.path.join(output_dir, z_matrix_filename), 'wb') as zfile:
        pickle.dump(z_matrix, zfile)

    # # visualize
    # print('Visualize')
    # visualize_dendrogram(kmeans_labels, z_matrix)

if __name__ == '__main__':

    print('Yallah Balagan...')
    main()
    print('Yallah bye...')