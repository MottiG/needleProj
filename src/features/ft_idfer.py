import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


class TfIdfer:
    """
    Build tf-ifd features for a given dataframe
    """

    def __init__(self):
        self.stopwords = stopwords.words('english')  # TODO remove important words from list

    def get_features(self, df: pd.DataFrame, cols: list, remove_stopwords: bool) -> pd.DataFrame:
        """
        for a given dataframe, create tf-idf vectors for each cell of each column specified in
        the "cols" :parameter.
        :param df: pandas dataframe contains the columns to preform tf-idf on them
        :param cols: list of columns names to get tf-idf vectors for this columns
        :param remove_stopwords: boolean to determine if stop-word should be remove before analyzing
        :return: a nwe dataframe, with index as input df and with columns as "cols" :parameter, contains the
         vectors of tf-idf.
        """
        df = df.fillna('')  # ignore nans
        features_df = pd.DataFrame(index=df.index.copy(), columns=cols)
        vectorizer = TfidfVectorizer(stop_words=self.stopwords if remove_stopwords else None)
        for col in cols:
            col_tf_idf = TfidfVectorizer().fit_transform(df[col])  # calc tf-idf
            features_df[col] = list(col_tf_idf)

        return features_df
