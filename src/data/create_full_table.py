import pickle
import os
import pandas as p

'''
This file creates a single table with the fields from all the files.
If for some field, there are several values of the same field (citations, categories, inventors), then the appropriate
column includes tuple of all the values that match the patent ID.

Outputs:
patent_table_clean.pickle - dataframe of the files that are present in all 5 files (intersection)
patent_table_with_nas.pickle - dataframe of the files that are present in at least 1 file (union)
'''

project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'raw', 'sample')
output_dir = os.path.join(project_dir, 'data', 'processed', 'sample')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#Reading the files
print("Loading the data")
authors_df = p.read_csv(os.path.join(input_dir, 'inventors.txt'), sep='\t')
citations_df = p.read_csv(os.path.join(input_dir, 'citations.txt'), sep='\t')
abstract_df = p.read_csv(os.path.join(input_dir, 'abstracts.txt'), sep='\t')
categories_df = p.read_csv(os.path.join(input_dir, 'categories.txt'), sep='\t')
patents_df = p.read_csv(os.path.join(input_dir, 'patents.txt'), sep='\t')

#Processing each file according to structure
print("Processing")
abstract_df.set_index('patentID', inplace=True)

authors_df['whole_name'] = authors_df.apply(lambda x: ' '.join((str(x['firstname']), str(x['lastname']))), axis=1)
authors_df= authors_df.groupby('patentID')['whole_name'].aggregate(lambda x: tuple(x))
authors_df = authors_df.to_frame('inventors')

citations_df = citations_df.groupby('citing')['cited'].aggregate(lambda x: tuple(x)).to_frame('citations')

categories_df['class'] = categories_df['class'].apply(lambda x: str(x).replace(" ", ""))
categories_df['class, mainclass'] = categories_df.apply(lambda x: (x['class'], x['mainclass']), axis=1)
categories_df = categories_df.groupby('patentID')['class, mainclass'].aggregate(lambda x: tuple(x)).to_frame()

patents_df.set_index('patentID', inplace=True)

#Joining and dumping
print("Dumping")
full_patent_table = patents_df.join(categories_df, how='outer').join(abstract_df, how='outer').join(authors_df, how='outer').join(citations_df, how='outer')
patent_no_nas = full_patent_table.dropna()

full_patent_table.reset_index(inplace=True)
patent_no_nas.reset_index(inplace=True)

full_patent_table.to_csv(os.path.join(output_dir, 'patent_table_with_nas.csv'), sep='\t')
patent_no_nas.to_csv(os.path.join(output_dir, 'patent_table_clean.csv'), sep='\t')


