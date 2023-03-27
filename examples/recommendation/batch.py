from src.data.movielens import MovieLens
from src.recommenders.item_knn import LenskitItemKNN
from src.recommenders.user_knn import LenskitUserKNN
from src.recommenders.bias import LenskitBias
from src.recommenders.biasedSVD import LenskitBiasedSVD
from src.recommenders.batch import LenskitBatch
import numpy as np
import pandas as pd
from src.utils import hrf_experiment_output_path

rec_temp_files_path = hrf_experiment_output_path().joinpath('rec_temp_files')

def main():
    movielens = MovieLens({
        'proportion': "ml-latest"
    })
  #  movielens.apply_filters()

    lenskit_batch = LenskitBatch()

    ratings = movielens.ratings
    ratings = ratings.sample(400000)
    ratings.to_csv("ratings-sample-400k-bias.csv")
    ratings.drop(columns=['timestamp'], inplace=True)


    item_knn = LenskitItemKNN({
        'maxNumberNeighbors': 10,
    })

    user_knn = LenskitUserKNN({
        'maxNumberNeighbors': 10
    })

    bias = LenskitBias({})
    biased_svd = LenskitBiasedSVD({
        'features': 10,
        'iterations': 20
    })

    items = ratings['item'].values
    users = ratings['user'].values

    print("usuários no total: ", users)
    print("usuários únicos: ", np.unique(users))
    unique_users = np.unique(users)
    user = unique_users[0]

   # item_knn.fit(ratings)
   # user_knn.fit(ratings)
    print(len(ratings))
    bias.fit(ratings)
    biased_svd.fit(ratings)

    #batch_predicted_result_item_knn = lenskit_batch.predict(item_knn.ItemKNN, ratings[['user', 'item']])
    #batch_predicted_result_user_knn = lenskit_batch.predict(user_knn.user_knn, ratings[['user', 'item']])

    batch_predicted_result_bias = lenskit_batch.predict(bias.Bias, ratings[['user', 'item']])
    batch_recommend_result_bias = lenskit_batch.recommend(bias.Bias, users, 10)

    batch_predicted_result_biased_svd = lenskit_batch.predict(biased_svd.BiasedMF, ratings[['user', 'item']])
    batch_recommend_result_biased_svd = lenskit_batch.recommend(biased_svd.BiasedMF, users, 10)

    batch_predicted_result_bias.to_csv("bias-predict-result-400k.csv")
    batch_recommend_result_bias.to_csv("bias-recommend-result-400k.csv")

    batch_predicted_result_biased_svd.to_csv("biasedSVD-predict-result-400k.csv")
    batch_recommend_result_biased_svd.to_csv("biasedSVD-recommend-result-400k.csv")


    """
    batch_recommend_result_user_knn = lenskit_batch.recommend(
        user_knn.user_knn,
        unique_users,
        10
    )
    batch_recommend_result_item_knn = lenskit_batch.recommend(
        item_knn.ItemKNN,
        unique_users,
        10
    )
    
    batch_predicted_result_item_knn.to_csv("ItemKNN-predict-result-400k.csv")
    batch_predicted_result_user_knn.to_csv("UserKNN-predict-result-400k.csv")
    batch_recommend_result_item_knn.to_csv("ItemKNN-recommend-result-400k.csv")
    batch_recommend_result_user_knn.to_csv("UserKNN-recommend-result-400k.csv")
    print("\n")

    """




if __name__ == '__main__':
    result = main()
