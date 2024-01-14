from lenskit.datasets import ML100K
from lenskit import batch, topn, util
import pandas as pd
from src.data.movielens import MovieLens
import recmetrics
from src.recommenders.user_knn import LenskitUserKNN
from sklearn.model_selection import train_test_split


from src.metrics.rmse import LenskitRMSE
from src.metrics.mae import  LenskitMAE
from src.metrics.novelty import  RecmetricsNOVELTY
from src.metrics.epc import  EPC

def example1():
    movielens = MovieLens({
        "proportion": "ml-latest-small",
        "filters":{}
    })

    ratings = movielens.ratings

    #print(ratings.head())

    ratings_usuario_1 = ratings[ratings['user'] == 1]

    #print("Ratings do usuário 1:")
    #print(ratings_usuario_1)

    num_itens_unicos = ratings['item'].nunique()

    #print("Número de itens únicos:", num_itens_unicos)

    avaliacoes_por_usuario = ratings.groupby('user')['item'].count()

    #print(avaliacoes_por_usuario)

    media_itens_por_usuario = avaliacoes_por_usuario.mean()

    #print(media_itens_por_usuario)

    y = ratings['rating']
    X = ratings.drop(columns=['timestamp'])

    #print("X: \n", X)
    #print("Y: \n", y)

    user_knn = LenskitUserKNN({
        'maxNumberNeighbors': 10
    })
    #Usar todos os dados para treinamento
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42)

    user_knn.fit(X_train)

    all_users = X['user'].unique()  # Substitua 'user_column_name' pelo nome da coluna que identifica os usuários

    recommendations_for_all_users = user_knn.recommend(all_users, n=10)  # Gerar recomendações para todos os usuários, recomendando 10 itens por usuário
    print("recomendations")
    print(recommendations_for_all_users)
    print(ratings.head())

    cutoff = 100
    epc = EPC(cutoff)

    #novelty = RecmetricsNOVELTY().evaluate(recommendations_for_all_users, ratings)
    novelty_epc = epc.evaluate(recommendations_for_all_users, ratings)

    print("RESULTADO")
    #print(novelty)
    print(novelty_epc)
    print("----------------------------------------------")


if __name__ == "__main__":
    example1()