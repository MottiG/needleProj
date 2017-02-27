import pandas as pd
import os
from scipy.cluster.hierarchy import fcluster
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics

def pull_patents(ind1, ind2, df):
    ind_list =[]
    if str(ind1) in df.index:
        ind_list.append(str(ind1))
    if str(ind2) in df.index:
        ind_list.append(str(ind2))
    return df.loc[ind_list, :]


def fpr_tpr_manual(patents_df, zmat, t, evaluation_table, ground_truth_label):
    clusters = fcluster(zmat, t)
    patents_df['final cluster'] = patents_df.apply(lambda x: clusters[int(x['kmeans_labels'])], axis=1)

    tp, fp, p, n  = 0.0, 0.0, 0.0, 0.0
    for index, pair in evaluation_table.iterrows():
        if str(pair['ind1']) in patents_df.index and str(pair['ind2']) in patents_df.index:
            cluster1 = patents_df.loc[str(pair['ind1']), 'final cluster']
            cluster2 = patents_df.loc[str(pair['ind2']), 'final cluster']

            if pair[ground_truth_label] == 1.0:
                p += 1
                if cluster1== cluster2:
                    tp += 1
            else:
                n += 1
                if cluster1== cluster2:
                    fp += 1


    tpr = tp/p if p>0 else 0.0
    fpr = fp/n if n>0 else 0.0

    return tpr, fpr


# SAMPLE = "sample"
#
# project_dir = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
# evaluation_file_name = os.path.join(project_dir, 'data', 'evaluation_table.txt')
# data_file_name = os.path.join(project_dir, 'data', 'processed', 'dendograms', 'kmeans_labels639.pickle')
# z_matrix_filename = os.path.join(project_dir, 'data', 'processed', 'dendograms', 'z_matrix639.pickle')
#
# kmeans_df = pd.read_pickle(data_file_name)
# evaluation_table = pd.read_csv(evaluation_file_name, sep='\t')
# z_matrix = pd.read_pickle(z_matrix_filename)


def evaluate_manual(kmeans_df, z_matrix, evaluation_table):
    evaluated_articles = pd.DataFrame(columns=kmeans_df.columns.values.tolist())

    for index, row in evaluation_table.iterrows():
        articles = pull_patents(row['ind1'], row['ind2'], kmeans_df)
        evaluated_articles = evaluated_articles.append(articles)

    print('Finished pulling the articles')

    t_range = np.linspace(0.8, 1.5, 200)
    tpr, fpr =  zip(*list(map(lambda t: fpr_tpr_manual(evaluated_articles, z_matrix,t, evaluation_table, 'Same Section'), t_range)))
    auc = metrics.auc(fpr, tpr)
    return fpr, tpr, auc



