from src.data.movielens import MovieLens
from src.preprocessing.normalize import NormalizeProcessing
from src.preprocessing.text import TextProcessing
from src.recommenders.item_knn import LenskitItemKNN
from src.recommenders.pop_score import LenskitPopScore
import numpy as np

if __name__ == "__main__":
    movielens = MovieLens({
        'proportion': "ml-latest-small"
    })


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

