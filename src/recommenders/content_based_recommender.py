from src.recommenders.recommender import Recommender
from lenskit.algorithms import Recommender as LenskitRecommender
from src.utils import process_parameters
from pandas import DataFrame, Series, concat
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
import numpy as np


class ContentBasedRecommender(Recommender):
    def __init__(self, parameters: dict) -> None:
        default_keys = {'feature', 'count_items'}
        parameters = process_parameters(parameters, default_keys)
        self.parameters = parameters
        self.feature = parameters.get('feature')
        self.similarity_matrix = None
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.mapping = None
        self.count_items = parameters.get('count_items') #Quantidade de itens para recomendar

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
        self.tf_idf(ratings, "genres")

    def recommend(self, users, n=None, candidates=None, n_jobs=None) -> DataFrame:

        #Os candidatos aqui podem ser os movie_input's


        candidates[self.feature].drop_duplicates(keep=False, inplace=True)


        recommend_df = DataFrame(columns=['item', 'recommended_items', self.feature])

        for title in candidates[self.feature]:

            temp_df = DataFrame(columns=['item', 'recommended_items', self.feature])
            movie_index = self.mapping[title]
            similarity_score = list(reversed(list(enumerate(self.similarity_matrix[movie_index]))))

            similarity_score = sorted(similarity_score, key=lambda x: x[0], reverse=True)
            similarity_score = similarity_score[1:self.count_items]
            movie_indices = [i[0] for i in similarity_score]
            recommend_result = candidates['title'].iloc[movie_indices]

            items_id = np.array(recommend_result.index.values)
            items_name = recommend_result.values

            items_id = Series(items_id)
            items_name = Series(items_name)

            recommended_items = [title] * self.count_items
            recommended_items = Series(recommended_items)
            temp_df['item'] = items_id
            temp_df['recommended_items'] = items_name
            temp_df[self.feature] = recommended_items
            recommend_df = concat([recommend_df, temp_df])


        return recommend_df




    def get_params(self, deep=True):
        pass

    def tf_idf(self, data: DataFrame, column_to_apply: str):
        column_to_indexing = "title"
        feature_to_indexing = data[column_to_indexing]
        feature = data[column_to_apply]
        feature_matrix = self.tfidf.fit_transform(feature)

        similarity_matrix = linear_kernel(feature_matrix, feature_matrix)

        # Mapping pode ir para a parte do algoritmo
        mapping = Series(data.index, index=feature_to_indexing)

        self.mapping = mapping
        self.similarity_matrix = similarity_matrix

