from src.data.bookcrossing import BookCrossing
from src.recommenders.bias import LenskitBias
from src.recommenders.biasedSVD import LenskitBiasedSVD
from src.recommenders.batch import LenskitBatch
from src.metrics.ndcg import NDCG
import numpy as np
from src.utils import hrf_experiment_output_path
from lenskit.metrics.predict import rmse

rec_temp_files_path = hrf_experiment_output_path().joinpath('rec_temp_files')

def main():
    bookcrossing = BookCrossing({})
    ratings = bookcrossing.ratings
    books = bookcrossing.items

    # Exclui colunas inúteis
    books.drop(['Image-URL-L', 'Image-URL-S', 'Image-URL-M', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10', 'Publisher'], axis=1, inplace=True)

    # Remove todas as linhas que tiverem o campo de Autor nulo
    books.dropna(subset=['Book-Author'], inplace=True)

    # Deixa no campo ano de publicação só valores numéricos e de 1965 até 2023
    books = books[books['Year-Of-Publication'].str.isnumeric() == True]
    books = books[(books['Year-Of-Publication'] > '1965') & (books['Year-Of-Publication'] < '2023')]

    lenskit_batch = LenskitBatch()

    # Livros com mais de 50 avaliações
    new_ratings = ratings.groupby('item').filter(lambda x: x['rating'].count() >= 50)

    bias = LenskitBias({})
    biased_svd = LenskitBiasedSVD({
        'features': 10,
        'iterations': 20
    })

    items = ratings['item'].values
    users = ratings['user'].values

    unique_users = np.unique(users)
    user = unique_users[0]

    bias.fit(new_ratings)
    biased_svd.fit(new_ratings)

    batch_predicted_result_bias = lenskit_batch.predict(bias.Bias, new_ratings[['user', 'item']])
    batch_recommend_result_bias = lenskit_batch.recommend(bias.Bias, users, 10)

    batch_predicted_result_biased_svd = lenskit_batch.predict(biased_svd.BiasedMF, new_ratings[['user', 'item']])
    batch_recommend_result_biased_svd = lenskit_batch.recommend(biased_svd.BiasedMF, users, 10)

    batch_predicted_result_bias.to_csv("bias-predict-result.csv")
    batch_recommend_result_bias.to_csv("bias-recommend-result.csv")

    batch_predicted_result_biased_svd.to_csv("biasedSVD-predict-result.csv")
    batch_recommend_result_biased_svd.to_csv("biasedSVD-recommend-result.csv")

if __name__ == '__main__':
    result = main()


