import pandas as pd
from src.data.movielens import MovieLens
from src.recommenders.moo import NSGA2PyMoo
from src.recommenders.moo import NSGA3PyMoo
from src.recommenders.moo import AGEMOEAPyMoo

def example1():
    movielens = MovieLens({
        "proportion": "ml-latest-small",
        "filters":{}
    })

    ratings = movielens.ratings
    movies = movielens.items

    # Processar 'genres' do DataFrame 'movies_df' para características binárias (one-hot encoding)
    genres = movies['genres'].str.get_dummies(sep='|')

    movies_genres = pd.concat([movies['movieId'], genres], axis=1)
    movies_genres = movies_genres.set_index('movieId')
    print(movies_genres)

    # Número de usuários
    num_users = ratings['user'].nunique()
    print("-------------------------------------")
    print(num_users)

    # Número de itens
    num_items = ratings['item'].nunique()
    print(num_items)

    print(ratings)
    cutoff = 50

    nsga2 = NSGA2PyMoo(cutoff,num_items,num_users,pop_size=5,n_gen=1,seed=2)
    recommendation = nsga2.recommend(users=num_users,n=cutoff,ratings=ratings, df_features=movies_genres)
    print("resultado")
    print(recommendation)

    '''nsga3 = NSGA3PyMoo(cutoff, num_items, num_users, pop_size=10, n_gen=1, num_partitions=12,seed=2)
    recommendation = nsga3.recommend(users=num_users, n=cutoff, ratings=ratings)
    print(recommendation)'''

    '''agemoea = AGEMOEAPyMoo(cutoff,num_items,num_users,pop_size=5,n_gen=1,seed=2)
    recommendation = agemoea.recommend(users=num_users,n=cutoff,ratings=ratings)
    print(recommendation)'''



if __name__ == "__main__":
    example1()