from src.visualization.static_bar import StaticBar
from src.visualization.static_scatter import StaticScatter
from src.data.movielens import MovieLens
import matplotlib.pyplot as plt
from src.utils import hrf_experiment_output_path
import seaborn as sns
import pandas as pd
import numpy as np
movielens = MovieLens(
    {
        'proportion': 'ml-latest-small',
        'filters': {}
    }
)
ratings = movielens.ratings
visualization_output_path = "visualization/static/bar/"
parameters = {
    'plot_types': {
        "ratings_by_user": True,
        "ratings_by_movie": True,
        "items_predict": True,
        "movie_ratings_distribution": True
    }
}

def items_most_rated_sns(ratings):
    value_counts_items = ratings['item'].value_counts()[0:10].reset_index().rename(
        columns={
            "index": "item",
            "item": "count"
        }
    )

    sns.histplot(value_counts_items, x="item", y='count')
    plt.show()
def items_most_rated(ratings):
    print("item most rated plot")
    value_counts_items = ratings['item'].value_counts().reset_index().rename(
        columns = {
            "index": "item",
            "item": "count"
        }
    )

    print(value_counts_items)
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(value_counts_items['item'], value_counts_items['count'])
    ax.set_title("Itens mais avaliados")
    ax.set_ylabel("Quantidade")
    ax.set_xlabel("Itens")
    archive_name = "itens_mais_avaliados.png"
    path_to_save = hrf_experiment_output_path().joinpath(visualization_output_path).joinpath(archive_name)
    fig.savefig(path_to_save)
    return value_counts_items


measure_rmse = pd.DataFrame(columns=['RMSE'])
measure_ndcg = pd.DataFrame(columns=['NDCG'])
measeure_mae = pd.DataFrame(columns=['MAE'])

rmse_values = np.array([
    1.458033,
    1.375486,
    1.344586,
    1.360211
])

ndcg_values = np.array([
0.058862,
0.062897,
7.274982,
6.960768
])



mae_values = np.array([
1.161295,
1.109742,
1.095435,
1.102076
])

rmse_values = pd.Series(rmse_values)
ndcg_values = pd.Series(ndcg_values)
mae_values = pd.Series(mae_values)


measure_rmse['RMSE'] = rmse_values
measure_ndcg['NDCG'] = ndcg_values
measeure_mae['MAE'] = mae_values
indexes = [
    'ItemKNN',
    'UserKNN',
    'Bias',
    'BiasedSVD'
]
measure_rmse.index = indexes
measure_ndcg.index = indexes
measeure_mae.index = indexes
def evaluate_measures_results(measure_df, metric):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(measure_df.index, measure_df[metric])
    ax.set_title("Comparativo entre valores de {} para os algoritmos de recomendação".format(metric))
    ax.set_ylabel("{}".format(metric))
    ax.set_xlabel("Algoritmos")
    archive_name = "{}.png".format(metric)
    path_to_save = hrf_experiment_output_path().joinpath(visualization_output_path).joinpath(archive_name)
    fig.savefig(path_to_save)


items_most_rated_sns(ratings)
items_most_rated(ratings)

evaluate_measures_results(measure_ndcg, "NDCG")
evaluate_measures_results(measeure_mae, "MAE")

static_bar = StaticBar(parameters)
static_bar.ratings_by_user_plot(ratings)
static_bar.ratings_by_movie_plot(ratings)


static_scatter = StaticScatter(parameters)
static_scatter.ratings_by_user_plot(ratings)
static_scatter.ratings_by_movie_plot(ratings)

