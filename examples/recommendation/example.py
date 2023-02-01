from src.data.movielens import MovieLens
from src.preprocessing.normalize import NormalizeProcessing
from src.preprocessing.text import TextProcessing
from src.recommenders.item_knn import LenskitItemKNN
from src.metrics.recall import LenskitRecall, ScikitRecall
from src.metrics.rmse import LenskitRMSE, ScikitRMSE
import numpy as np
import pandas as pd

movielens = MovieLens({
    'proportion': "ml-latest-small"
})

ratings = movielens.ratings
movies = movielens.items

normalize_processing = NormalizeProcessing({
    'norm': 'l2',
    'column_to_apply': "rating",
    'axis': 0
})

normalized_ratings = normalize_processing.pre_processing(ratings)
normalized_ratings.sample(1000)
normalized_ratings
text_processing = TextProcessing({
    'column_to_apply': 'genres',
    'remove_stop_words': True,
    'tokenize_words': True
})

movies2 = text_processing.pre_processing(movies)

item_knn = LenskitItemKNN({
    'maxNumberNeighbors': 20,
})

items = normalized_ratings['item'].values
users = normalized_ratings['user'].values
print("usuários no total: ", users)
print("usuários únicos: ", np.unique(users))
unique_users = np.unique(users)
user = unique_users[0]

item_knn.fit(normalized_ratings)

predict_to_user = item_knn.predict_for_user(user, items)
predict_to_user = predict_to_user[predict_to_user.notna()]
sorted_predicted_values_to_user = sorted(predict_to_user, reverse=True)
print(sorted_predicted_values_to_user)


lenskit_rmse = LenskitRMSE({
    "sample_weight": None,
    "squared": True,
    "missing": "error"
})
lenskit_recall = LenskitRecall({
    "labels": None,
    "average": "binary",
    "sample_weight": None,
    "zero_division": "warn"
})
scikit_rmse = ScikitRMSE({
    "sample_weight": None,
    "squared": True,
    "missing": "error"
})
scikit_recall = ScikitRecall({
    "labels": None,
    "average": "binary",
    "sample_weight": None,
    "zero_division": "warn"
})

flag_series = pd.Series()

recall_evaluate = lenskit_recall.evaluate(
    predictions=flag_series,
    truth=flag_series
)

