import os
import pandas as p
import pickle

'''
This file creates the dataframes from the txt files in /data/raw folder and saves them in /data/interim folder
'''


project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'raw', 'sample')
output_dir = os.path.join(project_dir, 'data', 'interim', 'sample')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

file_names = ['abstracts.txt', 'categories.txt', 'citations.txt', 'inventors.txt', 'patents.txt']

for raw_file_name in file_names:
    print('Importing ' + raw_file_name)
    file_name = os.path.join(input_dir, raw_file_name)
    dataframe= p.read_csv(file_name, sep='\t')

    output_file_name = raw_file_name[:-4] + '.pickle'
    file_name = os.path.join(output_dir, output_file_name)
    pickle.dump(dataframe, open( file_name, "wb"))

