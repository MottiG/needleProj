import pickle
import os
import pandas as pd

'''
This file creates a single table with the fields from all the files.
If for some field, there are several values of the same field (citations, categories, inventors), then the appropriate
column includes tuple of all the values that match the patent ID.

Outputs:
patent_table_clean.pickle - dataframe of the files that are present in all 5 files (intersection)
patent_table_with_nas.pickle - dataframe of the files that are present in at least 1 file (union)
'''

def split_class(class_string, main_class):
    class_string = class_string.lstrip()

    if 'D' in "".join(class_string.split(" ")):
        class_string = "".join(class_string.split(" "))
        return class_string[:3], class_string[3:]

    elif 'G9B' in class_string or 'PLT' in class_string:
        class_string = "".join(class_string.split(" "))
        return class_string[:3], class_string[3:]

    if ' ' in class_string:
        top_class = class_string.split(' ')[0]
        subclass = ''.join(class_string.split(' ')[1:])
    else:
        if len(class_string) ==6:
            top_class = class_string[:3]
            subclass = class_string[3:]
        else:
            if main_class:
                return float('nan'), float('nan')
            else:
                top_class = class_string[:-3]
                subclass = class_string[:-3]
    return top_class, subclass


def extract_classes(classes_list):
    main_top_class = float('nan')
    main_subclass = float('nan')
    other_classes = []

    for classtuple, mainclass in classes_list:
        if mainclass:
            main_top_class, main_subclass = classtuple
        else:
            other_classes.append(classtuple)

    return main_top_class, main_subclass, list(set(other_classes))

SAMPLE = ""

project_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'raw', SAMPLE)
output_dir = os.path.join(project_dir, 'data', 'processed', SAMPLE)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#Reading the files
print("Loading the data")
authors_df = pd.read_csv(os.path.join(input_dir, 'inventors.txt'), sep='\t')
citations_df = pd.read_csv(os.path.join(input_dir, 'citations.txt'), sep='\t')
abstract_df =pd.read_csv(os.path.join(input_dir, 'abstracts.txt'), sep='\t')
categories_df = pd.read_csv(os.path.join(input_dir, 'categories.txt'), sep='\t')
patents_df = pd.read_csv(os.path.join(input_dir, 'patents.txt'), sep='\t')

#Processing each file according to structure
print("Processing")
abstract_df.set_index('patentID', inplace=True)

authors_df['whole_name'] = authors_df.apply(lambda x: ' '.join((str(x['firstname']), str(x['lastname']))), axis=1)
authors_df= authors_df.groupby('patentID')['whole_name'].aggregate(lambda x: tuple(x))
authors_df = authors_df.to_frame('inventors')

citations_df = citations_df.groupby('citing')['cited'].aggregate(lambda x: tuple(x)).to_frame('citations')

categories_df['class, mainclass'] = categories_df.apply(lambda x: (split_class(x['class'], bool(x['mainclass'])), x['mainclass']), axis=1)
categories_df = categories_df.groupby('patentID')['class, mainclass'].aggregate(lambda x: tuple(x)).to_frame()
categories_df['main top class'], categories_df['main subclass'], categories_df['other classes'] = \
    zip(*categories_df['class, mainclass'].apply(extract_classes))

patents_df.set_index('patentID', inplace=True)

#Joining and dumping

full_patent_table = patents_df.join(categories_df, how='outer').join(abstract_df, how='outer').join(authors_df, how='outer').join(citations_df, how='outer')
patent_no_nas = full_patent_table.dropna()

print("No. of patents: " + str(len(patents_df)))
print("No. of abstracts: " + str(len(abstract_df)))
print("Final length: " + str(len(patent_no_nas)))
print("Dumping")
pd.to_pickle(patent_no_nas, os.path.join(output_dir, 'patent_table_clean_new.pickle'))

patent_no_nas = patent_no_nas.drop('abstract', 1)

pd.to_pickle(patent_no_nas, os.path.join(output_dir, 'patent_table_clean_new_no_abstract.pickle'))
