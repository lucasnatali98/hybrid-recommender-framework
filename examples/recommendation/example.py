from src.data.movielens import MovieLens
from src.preprocessing.normalize import NormalizeProcessing
from src.preprocessing.text import TextProcessing
from src.recommenders.item_knn import LenskitItemKNN


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
user = users[0]

item_knn.fit(normalized_ratings)

predict_to_user = item_knn.predict_for_user(user, items)
predict_to_user = predict_to_user[predict_to_user.notna()]
print(predict_to_user)
