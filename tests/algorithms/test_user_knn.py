import pandas as pd
import pytest
from lenskit.algorithms.basic import UnratedItemCandidateSelector
import numpy as np
from src.data.movielens import MovieLens
from src.recommenders.user_knn import UserKNN
from lenskit.algorithms.user_knn import UserUser
from lenskit.algorithms.ranking import TopN
from lenskit.algorithms.user_knn import UserUser
movielens = MovieLens({
    'proportion': 'ml-latest-small',
    'filters': {}
})

ratings = movielens.ratings[0:1000]

parameters = {
    "maxNumberNeighbors": 1,
    "minNumberNeighbors": 2,
    "min_sim": "",
    "feedback": "implicit",
    "aggregate": "weighted-average",
    "use_ratings": True
}
user = UserKNN(parameters)


class TestUserKNN:
    def test_fit(self):
        pass

    def test_recommend(self):
        users = np.unique(ratings['user'].values)
        items = ratings['item'].values

        select = UnratedItemCandidateSelector()
        user.fit(ratings)
        top_n = TopN(user.user_knn, select)

        topn_dataframe = pd.DataFrame(columns=['user', 'item', 'score'])

        print("topn_dataframe")
        print(topn_dataframe)
        number_of_items_rankeds = 10
        for u in users:
            recs = top_n.recommend(
                u,
                number_of_items_rankeds,
                items
            )

            user_id = [u] * number_of_items_rankeds
            recs['user'] = pd.Series(user_id)
            topn_dataframe = pd.concat([topn_dataframe, recs], ignore_index=True)

            print(topn_dataframe)

    def test_predict(self):
        pass

    def test_predict_for_users(self):

        user.fit(ratings)

        preds = user.predict_for_user(1, [
            10, 20, 30, 40, 50, 60,70,
            80,90,100,120,130
        ])

        print("Preds: ", preds)

