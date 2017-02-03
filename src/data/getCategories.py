""" The package snap.py works on python 2.7 only """

from collections import Counter, defaultdict

import matplotlib.pyplot as plt


try:
   import cPickle as pickle
except:
   import pickle
import os
from numpy import linspace as lrange


'''
This file create dictionary of categories exists in the database
'''

__author__ = 'slouis'
'''
This file reads in/out degree distributions of the citation graph.
The nodes are from both files: patent.txt & citations.txt files (to ensure we have also nodes of degree 0.

Outputs:
'''

project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'raw')
output_dir = os.path.join(project_dir, 'data', 'processed')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
LIMIT_NUM_ROWS = float("inf") #float("inf") #

print("Loading the data")
CATEGORIES_FILE_PATH = os.path.join(input_dir, 'categories.txt')

categories = defaultdict(int)
main_categories = defaultdict(int)

print("Reading categories file")
with open(CATEGORIES_FILE_PATH, mode='r') as vf:
    next(vf)
    row_counter = 0
    for line in vf:
        if row_counter % 100000 == 0 : print(row_counter)
        row_counter +=1
        splittedRow = line.strip().split()
        if splittedRow[-1]=="1" : main_categories["".join(splittedRow[1:-1])] += 1
        categories["".join(splittedRow[1:-1])] += 1
        if row_counter >= LIMIT_NUM_ROWS:
            break

pickle.dump(categories,open(os.path.join(output_dir, 'categories_in_db_'+ str(row_counter)+'.pickle'),'wb'))
pickle.dump(main_categories,open(os.path.join(output_dir, 'main_categories_in_db_'+ str(row_counter)+'.pickle'),'wb'))

print('done.')
pass