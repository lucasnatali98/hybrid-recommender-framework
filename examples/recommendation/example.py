from src.data.movielens import MovieLens
from src.preprocessing.normalize import NormalizeProcessing
from src.preprocessing.text import TextProcessing
from src.recommenders.item_knn import LenskitItemKNN
from src.metrics.recall import LenskitRecall, ScikitRecall
from src.metrics.rmse import LenskitRMSE, ScikitRMSE
from src.recommenders.batch import LenskitBatch
import numpy as np
import pandas as pd

movielens = MovieLens({
    'proportion': "ml-latest-small"
})

lenskit_batch = LenskitBatch()

ratings = movielens.ratings
ratings.drop(columns=['timestamp'], inplace=True)
movies = movielens.items

normalize_processing = NormalizeProcessing({
    'norm': 'l2',
    'column_to_apply': "rating",
    'axis': 0
})




text_processing = TextProcessing({
    'column_to_apply': 'genres',
    'remove_stop_words': True,
    'tokenize_words': True
})

movies2 = text_processing.pre_processing(movies)

item_knn = LenskitItemKNN({
    'maxNumberNeighbors': 10,
})

items = ratings['item'].values
users = ratings['user'].values

print("usuários no total: ", users)
print("usuários únicos: ", np.unique(users))
unique_users = np.unique(users)
user = unique_users[0]

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

ratings_by_itemid = ratings.drop(columns=['user'])
ratings_by_itemid = ratings_by_itemid.set_index('item')


item_knn.fit(ratings)


batch_predicted_result = lenskit_batch.predict(item_knn.ItemKNN, ratings[['user', 'item']])
print(batch_predicted_result)

predict_to_user = item_knn.predict_for_user(user, items)
predict_to_user = predict_to_user[predict_to_user.notna()]
print(predict_to_user)




flag_series = pd.Series(dtype=float)

recall_evaluate = lenskit_recall.evaluate(
    predictions=flag_series,
    truth=flag_series
)
