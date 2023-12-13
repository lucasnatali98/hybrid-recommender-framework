from lenskit.datasets import ML100K
from lenskit import batch, topn, util
from lenskit import crossfold as xf
from lenskit.algorithms import Recommender, als, item_knn as knn
import pandas as pd
from src.data.movielens import MovieLens
import recmetrics
from src.recommenders.user_knn import LenskitUserKNN
from sklearn.model_selection import train_test_split


from src.metrics.rmse import LenskitRMSE
from src.metrics.mae import  LenskitMAE
from src.metrics.diversity import  RecmetricsDIVERSITY
from src.metrics.diversity import  GiniIndexDIVERSITY


def example1():
    movielens = MovieLens({
        "proportion": "ml-latest-small",
        "filters":{}
    })

    ratings = movielens.ratings
    movies = movielens.items
    print(movies.head())
    print(ratings.head())

    # Processar 'genres' do DataFrame 'movies_df' para características binárias (one-hot encoding)
    genres = movies['genres'].str.get_dummies(sep='|')
    print(genres)

    # Criar DataFrame apenas com características de gêneros
    movies_genres = pd.concat([movies['movieId'], genres], axis=1)
    movies_genres = movies_genres.set_index('movieId')  # Definir 'movieId' como índice

    print(movies_genres)

    y = ratings['rating']
    X = ratings.drop(columns=['timestamp'])

    print("X: \n", X)
    print("Y: \n", y)

    user_knn = LenskitUserKNN({
        'maxNumberNeighbors': 10
    })

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

    user_knn.fit(X_train)

    all_users = X['user'].unique()  # Substitua 'user_column_name' pelo nome da coluna que identifica os usuários

    recommendations_for_all_users = user_knn.recommend(all_users, n=100)  # Gerar recomendações para todos os usuários, recomendando 10 itens por usuário

    print("recomendations")
    print(recommendations_for_all_users.head())
    print(movies_genres)
    diversity = RecmetricsDIVERSITY().evaluate(recommendations_for_all_users, movies_genres)
    #diversity2 = GiniIndexDIVERSITY().evaluate(recommendations_for_all_users, )

    print("TESTE")
    print(diversity)
    print("----------------------------------------------")



if __name__ == "__main__":
    example1()