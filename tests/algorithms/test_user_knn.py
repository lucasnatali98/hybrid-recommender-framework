import pytest
from lenskit.algorithms.basic import UnratedItemCandidateSelector

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
        users = ratings['user'].values
        items = ratings['item'].values
        uu = UserUser(10)
        print("VAI TOMAR NO MEIO DO CU")

        print("NASDHJAFSDJ[")
        select = UnratedItemCandidateSelector()
        uu.fit(ratings)
        top_n = TopN(uu, select)


        for u in users:
            print("Usuário ID: ", u)
            recs = top_n.recommend(
                u,
                10,
                items
            )
            print("recs: ", recs)

    def test_predict(self):
        pass

    def test_predict_for_users(self):

        user.user_knn.fit(ratings)

        preds = user.user_knn.predict_for_user(1, [
            10, 20, 30, 40, 50, 60,70,
            80,90,100,120,130
        ])

        print("Preds: ", preds)

