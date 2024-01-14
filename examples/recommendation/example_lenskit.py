from lenskit.datasets import ML100K
from lenskit import batch, topn, util
from lenskit import crossfold as xf
from lenskit.algorithms import Recommender, als, item_knn as knn
import pandas as pd
from src.data.movielens import MovieLens


def example1():
    movielens = MovieLens({
        "proportion": "ml-latest-small",
        "filters":{}
    })
    ratings = movielens.ratings

    print(ratings.head())

    algo_ii = knn.ItemItem(20)
    algo_als = als.BiasedMF(50)

    all_recs = []
    test_data = []
    for train, test in xf.partition_users(ratings[['user', 'item', 'rating']], 5, xf.SampleFrac(0.2)):
        test_data.append(test)
        all_recs.append(evaluate('ItemItem', algo_ii, train, test))
        all_recs.append(evaluate('ALS', algo_als, train, test))


    all_recs = pd.concat(all_recs, ignore_index=True)
    test_data = pd.concat(test_data, ignore_index=True)
    print("all recs head: ")
    print(all_recs.head())

    print("\n")
    print("test data: ")
    print(test_data.head())


    rla = topn.RecListAnalysis()
    rla.add_metric(topn.ndcg)
    rla.add_metric(topn.dcg)
    rla.add_metric(topn.recall)

    results = rla.compute(all_recs, test_data)
    print("results")
    print(results.head())


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