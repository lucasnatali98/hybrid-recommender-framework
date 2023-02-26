from src.data.movielens import MovieLens
from src.recommenders.item_knn import LenskitItemKNN
from src.recommenders.batch import LenskitBatch
import numpy as np
import pandas as pd

def main():
    movielens = MovieLens({
        'proportion': "ml-latest-small"
    })

    lenskit_batch = LenskitBatch()

    ratings = movielens.ratings
    ratings.drop(columns=['timestamp'], inplace=True)


    item_knn = LenskitItemKNN({
        'maxNumberNeighbors': 10,
    })

    items = ratings['item'].values
    users = ratings['user'].values

    print("usuários no total: ", users)
    print("usuários únicos: ", np.unique(users))
    unique_users = np.unique(users)
    user = unique_users[0]

    item_knn.fit(ratings)

    batch_predicted_result = lenskit_batch.predict(item_knn.ItemKNN, ratings[['user', 'item']])

    batch_recommend_result = lenskit_batch.recommend(
        item_knn.ItemKNN,
        unique_users,
        10
    )

    print("Batch predict result")
    print(batch_predicted_result)
    print("\n")

    batch_predicted_result.to_csv("batch_predict_result.csv")

    print("Batch recommend result")
    print(batch_recommend_result)
    print("\n")
    return batch_predicted_result


if __name__ == '__main__':
    result = main()
    print(result)
