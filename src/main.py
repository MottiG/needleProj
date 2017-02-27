import pandas as pd
import os
from features.build_features import build_features
from models.build_clusters import build_clusters
from evaluation.manual_evaluation import evaluate_manual
import pickle
from visualization.visualize import visualize_dendrogram
import time


def main():
    # for running on full data set SAMPLE = ""
    SAMPLE = ""
    df_file_name = 'patent_table_clean_new'

    # features parameters
    cols_of_tfidf = ['abstract']  # name of columns to apply tfidf vectorization
    minimal_community_size = 2
    n_components = 150  # number of components to save after dimension reducing of tfidf matrices
    k_means = 639  # number of cluster to be the base of the hierarchical clustering


    # Load data
    project_dir = os.path.abspath(os.path.join(__file__, '..', '..'))
    input_dir = os.path.join(project_dir, 'data', 'processed', SAMPLE)
    output_dir = os.path.join(project_dir, 'data', 'processed', 'dendograms', SAMPLE)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if SAMPLE:
        kmeans_labels_filename = 'kmeans_labels '+df_file_name+'.pickle'
        z_matrix_filename = 'z_matrix '+df_file_name+'.pickle'
    else:
        kmeans_labels_filename = 'kmeans_labels' + str(k_means) + 'tfidf' + '.pickle'
        z_matrix_filename = 'z_matrix' + str(k_means) + 'tfidf' + '.pickle'

    print('Loading data')
    df = pd.read_pickle(os.path.join(input_dir, df_file_name+'.pickle'))


    # Create features
    t0 = time.time()
    print('Building features')
    features_matrix = build_features(df, cols_of_tfidf, n_components, minimal_community_size)
    print("Features building total running time is: {} ".format(time.time() - t0))

    print('Building clusters')
    t0 = time.time()
    kmeans_labels, z_matrix = build_clusters(features_matrix, pd.DataFrame(index=df.index.copy()), k_means)
    print ("Clusters building running time is: {} ".format(time.time() - t0))

    print('Saving kmeans labels as', kmeans_labels_filename)
    pd.to_pickle(kmeans_labels, os.path.join(output_dir, kmeans_labels_filename))
    print('Saving z matrix as', z_matrix_filename)
    with open(os.path.join(output_dir, z_matrix_filename), 'wb') as zfile:
        pickle.dump(z_matrix, zfile)

    #evaluate
    evaluation_file_name = os.path.join(project_dir, 'data', 'evaluation_table.txt')
    evaluation_table = pd.read_csv(evaluation_file_name, sep='\t')
    fpr, tpr, auc = evaluate_manual(kmeans_labels, z_matrix, evaluation_table)
    print("AUC of ROC curve: %f" % auc)

    with open(os.path.join(output_dir, ('tpr_fpr' + 'tfidf' + '.pickle')), 'wb') as tpr_file:
        pickle.dump((fpr, tpr), tpr_file)

    # visualize
    print('Visualize')
    visualize_dendrogram(kmeans_labels, z_matrix)

if __name__ == '__main__':

    print('Yallah Balagan...')
    main()
    print('Yallah bye...')