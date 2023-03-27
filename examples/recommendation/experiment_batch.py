from src.data.movielens import MovieLens
from src.recommenders.item_knn import LenskitItemKNN
from src.recommenders.user_knn import LenskitUserKNN
from src.recommenders.bias import LenskitBias
from src.recommenders.biasedSVD import LenskitBiasedSVD
from src.recommenders.batch import LenskitBatch
from sklearn.model_selection import train_test_split
from src.preprocessing.normalize import NormalizeProcessing
import numpy as np
import pandas as pd
from src.utils import hrf_experiment_output_path

rec_temp_files_path = hrf_experiment_output_path().joinpath('rec_temp_files')


def main():

    lenskit_batch = LenskitBatch()
    normalizer = NormalizeProcessing({
        'norm': 'l2',
        'column_to_apply': 'rating'
    })
    #

    ratings = pd.read_csv("../../experiment_output/rec_temp_files/ratings-200k.csv", index_col=[0])
    print("Ratings, normal: \n", ratings)
#    ratings = normalizer.pre_processing(ratings)

 #   print("Ratings normalize: \n", ratings)
    y = ratings['rating']
    X = ratings.drop(columns=['timestamp'])

    print("X: \n", X)
    print("Y: \n", y)


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

    unique_users = np.unique(users)
    user = unique_users[0]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 42)


    print("X test: \n", X_test)
    item_knn.fit(X_train)
    user_knn.fit(X_train)
    bias.fit(X_train)
    biased_svd.fit(X_train)

    batch_predicted_result_item_knn = lenskit_batch.predict(item_knn.ItemKNN, X_test)
    batch_predicted_result_user_knn = lenskit_batch.predict(user_knn.user_knn, X_test)

    batch_recommend_result_item_knn = lenskit_batch.recommend(item_knn.ItemKNN, users, 10)
    batch_recommend_result_user_knn = lenskit_batch.recommend(user_knn.user_knn, users, 10)

    batch_predicted_result_bias = lenskit_batch.predict(bias.Bias, X_test)
    batch_recommend_result_bias = lenskit_batch.recommend(bias.Bias, users, 10)

    batch_predicted_result_biased_svd = lenskit_batch.predict(biased_svd.BiasedMF, X_test)
    batch_recommend_result_biased_svd = lenskit_batch.recommend(biased_svd.BiasedMF, users, 10)

    batch_predicted_result_item_knn.to_csv("ItemKNN-predict-result-final-200k.csv")
    batch_recommend_result_item_knn.to_csv("ItemKNN-recommend-result-final-200k.csv")

    batch_predicted_result_user_knn.to_csv('UserKNN-predict-result-final-200k.csv')
    batch_recommend_result_user_knn.to_csv("UserKNN-recommend-result-final-200k.csv")

    batch_predicted_result_bias.to_csv("bias-predict-result-final-200k.csv")
    batch_recommend_result_bias.to_csv("bias-recommend-result-final-200k.csv")

    batch_predicted_result_biased_svd.to_csv("biasedSVD-predict-result-final-200k.csv")
    batch_recommend_result_biased_svd.to_csv("biasedSVD-recommend-result-final-200k.csv")


if __name__ == '__main__':
    result = main()
