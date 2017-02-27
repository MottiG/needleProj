from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import os, pickle

class TfIdfer:
    """
    Build tf-ifd features for a given dataframe
    """

    def __init__(self):
        self.stopwords = stopwords.words('english')

    def get_features(self, df, cols: list,
                     remove_stopwords: bool = True, max_df: float = 1.0, min_df: float = 1) -> dict:
        """
        for a given dataframe, create tf-idf matrices for each columns specified in the "cols" parameter.
        :param df: pandas dataframe contains the columns to preform tf-idf on them
        :param cols: list of columns names to get tf-idf vectors for this columns
        :param remove_stopwords: boolean to determine if stop-word should be remove before analyzing.  default=True
        :param max_df: float in range [0.0, 1.0] or int, default=1.0
        :param min_df: float in range [0.0, 1.0] or int, default=1
        :return: dictionary with keys as columns of "cols" and values contains the matrices of tf-idf.
        """

        project_dir = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
        features_dict_file = os.path.join(project_dir, 'models', 'tf_idf_features_dict.pickle')
        models_file = os.path.join(project_dir, 'models', 'tf_idf_vectorizers.pickle')

        df = df.fillna('')  # ignore nans
        features_dict = {}
        vectorizers_dict = {}

        for col in cols:
            print('----calculating tfidf of column: ', col)
            vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df, sublinear_tf=True,
                                         stop_words=self.stopwords if remove_stopwords else None)
            features_dict[col] = vectorizer.fit_transform(df[col])  # calc tf-idf
            vectorizers_dict[col] = vectorizer

        pickle.dump(features_dict, open(features_dict_file, 'wb'))
        pickle.dump(vectorizers_dict, open(models_file, 'wb'))

        return features_dict
