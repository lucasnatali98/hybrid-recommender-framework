from src.data.steam import steamDB
from src.preprocessing.normalize import NormalizeProcessing
from src.preprocessing.text import TextProcessing
from src.recommenders.item_knn import LenskitItemKNN
from src.recommenders.scikit_svd import LenskitScikitSVD
from src.recommenders.pop_score import LenskitPopScore
from src.recommenders.biasedSVD import LenskitBiasedSVD

import csv

import numpy as np

if __name__ == "__main__":
    steamModel = steamDB({
        "proportion": "steam"
        }
    )
    ratings = steamModel.ratings
    games = steamModel.items

    print("scikit: ")

    pop_score = LenskitPopScore({
        'score_method': 'quantile'
    })

    items = ratings['item'].values
    users = ratings['user'].values

    unique_users = np.unique(users)
    user = unique_users[0]

    pop_score.fit(ratings)

    predict = pop_score.predict(ratings[['user', 'item']])
    print("Predict")
    print(predict)

    recommend_to_users = pop_score.recommend(unique_users, 10)

    print("Recommend")
    print(recommend_to_users)

    recommend_to_users.to_csv('dados.csv')


