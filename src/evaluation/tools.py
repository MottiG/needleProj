import os
import pandas as pd

def dendrogram_to_list(dendrogram, df, top_level_label):
    title_dict = dict.fromkeys(dendrogram[top_level_label].unique())
    for top_class in dendrogram[top_level_label].unique():
        patents = df[dendrogram[top_level_label] == top_class]
        titles = patents['title'].tolist()
        title_dict[top_class] = titles

    return title_dict

dendrogram_path = 'C:\\Users\\Maria\\Documents\\GitHub\\needleProj\\data\\processed\\dendograms\\dendogram sample 100-7.pickle'
dataframe_path = 'C:\\Users\\Maria\\Documents\\GitHub\\needleProj\\data\\processed\\sample\\patent_table_new_10k.pickle'

dendrogram = pd.read_pickle(dendrogram_path)
dataframe = pd.read_pickle(dataframe_path)

title_dict = dendrogram_to_list(dendrogram, dataframe, 7)
for title in title_dict:
    print('%s:' % title)
    title_list = title_dict[title]
    for title in title_list:
        print(title)

