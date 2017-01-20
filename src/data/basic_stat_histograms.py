import pandas as p
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import os

project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'processed')
output_dir = os.path.join(project_dir, 'reports', 'figures', 'basic_stats')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def plot_histogram(data, title, figname):
    plt.hist(data, bins=30)
    ax = plt.gca()
    ax.set_yscale('log')
    ax.set_title(title)
    plt.savefig(os.path.join(output_dir, (figname + '.png')))


df = p.read_pickle(os.path.join(input_dir, 'patent_table_clean.pickle'))

df['inventor_freq'] = df.apply(lambda x: Counter(x['inventors']), axis=1)
data = list(df['inventor_freq'].sum().values())
plot_histogram(data, 'Inventors frequency', 'inventor_frequency')


df['category_freq']= df.apply(lambda x: Counter(x['class, mainclass']), axis=1)
data = list(df['category_freq'].sum().values())
plot_histogram(data, 'Category frequency (the frequency of the given mainclass pair)', 'category_frequency')


df['out_degree'] = df.apply(lambda x: len(x['citations']), axis=1)
data = np.array(df['out_degree'])
plot_histogram(data, 'Out-degree of a patent', 'out_degree')

df['citation_freq'] = df.apply(lambda x: Counter(x['citations']), axis=1)
data = list(df['citation_freq'].sum().values())
plot_histogram(data, 'In-degree of a patent', 'in_degree')






