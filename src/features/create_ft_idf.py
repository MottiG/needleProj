import pandas as pd
import os
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


'''
create tf-ifd feature of for a given column of the patent_table_clean dataframe
'''
stopw = stopwords.words('english')  # TODO remove important words from list
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
input_dir = os.path.join(project_dir, 'data', 'processed', 'sample')
df = pd.read_pickle(os.path.join(input_dir, 'patent_table_clean.pickle'))


class TfIdfer:

    def get_features(df: pd.DataFrame, cols: list, remove_stopwords: bool) -> pd.dataFrame:
        features = pd.DataFrame(index=df.index.copy(), columns=cols)
        for col in cols: # TODO check if can work on all cols without loop!
            if remove_stopwords:
                df[col].apply(lambda x: [item for item in x if item not in stopw])  # TODO check it, looks like item is letters

            # TODO create tfidf feature x and assign list(x) to features[col]


