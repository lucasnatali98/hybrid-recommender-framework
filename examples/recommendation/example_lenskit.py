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

def example1():
    movielens = MovieLens({
        "proportion": "ml-latest-small",
        "filters":{}
    })
    rmse = LenskitRMSE({
        "sample_weight": "None",
        "squared": True,
        "missing": "error"
    })

    mae = LenskitMAE({
        "multioutput": "uniform_average"
    })
    ratings = movielens.ratings

    print(ratings.head())

    ratings_usuario_1 = ratings[ratings['user'] == 1]

    print("Ratings do usuário 1:")
    print(ratings_usuario_1)

    num_itens_unicos = ratings['item'].nunique()

    print("Número de itens únicos:", num_itens_unicos)

    avaliacoes_por_usuario = ratings.groupby('user')['item'].count()

    print(avaliacoes_por_usuario)

    media_itens_por_usuario = avaliacoes_por_usuario.mean()

    print(media_itens_por_usuario)

    '''algo_ii = knn.ItemItem(20)
    print("algo_ii")
    print(algo_ii)
    algo_als = als.BiasedMF(50)


    all_recs = []
    test_data = []
    for train, test in xf.partition_users(ratings[['user', 'item', 'rating']], 5, xf.SampleFrac(0.2)):
        test_data.append(test)
        all_recs.append(evaluate('ItemItem', algo_ii, train, test))
        print(test_data)
        #all_recs.append(evaluate('ALS', algo_als, train, test))

    print(xf.partition_users(ratings[['user', 'item', 'rating']], 5, xf.SampleFrac(0.2)))

    all_recs = pd.concat(all_recs, ignore_index=True)
    test_data = pd.concat(test_data, ignore_index=True)
    print("all recs head: ")
    print(all_recs.head())

    print("\n")
    print("test data: ")
    print(test_data.head())'''

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

    recommendations_for_all_users = user_knn.recommend(all_users, n=10)  # Gerar recomendações para todos os usuários, recomendando 10 itens por usuário

    print(recommendations_for_all_users.head())

    #Prediction list
    rec_lists = {}
    for user, item, _, _ in recommendations_for_all_users.itertuples(index=False):
        if user not in rec_lists:
            rec_lists[user] = []
        # Verifica se o item não é NaN e é um número
        if not pd.isnull(item) and pd.notnull(pd.to_numeric(item, errors='coerce')):
            rec_lists[user].append(int(item))  # Convert item to int

    #print('rec list 1')
    #print(rec_lists)

    rec_lists = [rec_list for rec_list in rec_lists.values()]
    print('rec list 2')
    print(rec_lists)

    #print(ratings['item'].unique())

    #Pop
    nov = ratings.item.astype(int).value_counts()
    pop = dict(nov)
    print("pop")
    print(pop)

    # Print the types of items in rec_lists
    #print("Type of items in rec_lists:")
    #for rec_list in rec_lists:
        #print(type(rec_list[0]))

    # Print the types of keys in pop
    #print("Type of keys in pop:")
    #for key in pop.keys():
        #print(type(key))

    #for i in pop.keys():
        #try:
            #int(i)
       # except ValueError:
           # print(f"Invalid item ID: {i}")


    #U -  num de usuarios
    num_users = ratings['user'].nunique()
    print("u")
    print(num_users)

    #N - tamanho da lista
    tamanhos_listas = [len(items) for items in rec_lists]
    tamanho_medio = sum(tamanhos_listas) / len(tamanhos_listas)
    n = int(round(tamanho_medio))
    print('n')
    print(n)

    random_novelty, random_list = recmetrics.novelty(rec_lists, pop, num_users, n)

    print("TESTE")
    print(random_novelty)
    print("----------------------------------------------")
    print(random_list)

    #rla = topn.RecListAnalysis()
    #rla.add_metric(topn.ndcg)
    #rla.add_metric(topn.dcg)
    #rla.add_metric(topn.recall)

    #results = rla.compute(all_recs, test_data)
    #print("results")
    #print(results.head())


def evaluate(aname, algo, train, test):
    fittable = util.clone(algo)
    fittable = Recommender.adapt(fittable)
    fittable.fit(train)
    users = test.user.unique()
    # now we run the recommender
    recs = batch.recommend(fittable, users, 100)
    # add the algorithm name for analyzability
    recs['Algorithm'] = aname
    return recs


if __name__ == "__main__":
    example1()