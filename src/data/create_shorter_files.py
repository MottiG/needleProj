import pandas as p
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import os

SAMPLE = ""

project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'processed', SAMPLE)
df_file_name = 'patent_table_clean_new.pickle'
output_dir = os.path.join(project_dir, 'data', 'processed','sample')
out_file_name = 'class_counts.txt'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df = p.read_pickle(os.path.join(input_dir, df_file_name))

df_10k = df[:10000]
p.to_pickle(df_10k, os.path.join(output_dir, 'patent_table_new_10k.pickle'))

df_50k = df[:50000]
p.to_pickle(df_10k, os.path.join(output_dir, 'patent_table_new_50k.pickle'))