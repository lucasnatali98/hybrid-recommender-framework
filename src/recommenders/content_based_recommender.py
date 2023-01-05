from src.recommenders.recommender import Recommender
from lenskit.algorithms import Recommender as LenskitRecommender
from src.utils import process_parameters
from pandas import DataFrame, Series
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel


class ContentBasedRecommender(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        self.parameters = parameters

    def predict_for_user(self, user, items, ratings=None):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        pass

    def predict(self, pairs, ratings):
        """

        @param user:
        @param items:
        @return:
        """
        pass

    def fit(self, ratings: DataFrame, **kwargs):
        """

        @param ratings:
        @param kwargs:
        @return:
        """
        pass

    def recommend(self, users, n=None, candidates=None, n_jobs=None) -> DataFrame:
        pass

    def get_params(self, deep=True):
        pass

    def tf_idf(self, data: DataFrame, column_to_apply: str):
        column_to_indexing = "title"
        feature_to_indexing = data[column_to_indexing]
        feature = data[column_to_apply]
        feature_matrix = self.tfidf.fit_transform(data)
        print("Feature Matrix")
        print(feature_matrix)
        similarity_matrix = linear_kernel(feature_matrix, feature_matrix)

        # Mapping pode ir para a parte do algoritmo
        mapping = pd.Series(data.index, index=feature_to_indexing)
        print("Similarity matrix")
        print(similarity_matrix)
        #similarity_matrix.to_csv(self.text_processing_output_path)
        return data
