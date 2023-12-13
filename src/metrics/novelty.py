from src.metrics.metric import NoveltyMetric
from typing import List
import recmetrics
import pandas as pd


class NOVELTY(NoveltyMetric):
    """

    """
    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        raise NotImplementedError


class RecmetricsNOVELTY(NOVELTY):
    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs): #recomendações e ratings
        # Prediction list
        rec_lists = {}
        for user, item, _, _ in predictions.itertuples(index=False):
            if user not in rec_lists:
                rec_lists[user] = []
            # Verifica se o item não é NaN e é um número
            if not pd.isnull(item) and pd.notnull(pd.to_numeric(item, errors='coerce')):
                rec_lists[user].append(int(item))  # Convert item to int
        rec_lists = [rec_list for rec_list in rec_lists.values()]
        print('rec list 2')
        print(rec_lists)

        # Pop
        nov = truth.item.astype(int).value_counts()
        pop = dict(nov)
        print("pop")
        print(pop)

        # U -  num de usuarios
        num_users = truth['user'].nunique()
        print("u")
        print(num_users)

        # N - tamanho da lista
        list_sizes = [len(items) for items in rec_lists]
        average_size = sum(list_sizes) / len(list_sizes)
        average_size_int = int(round(average_size))
        print('n')
        print(average_size_int)

        novelty_value, novelty_list = recmetrics.novelty(rec_lists, pop, num_users, average_size_int)
        print("TESTE")
        print(novelty_value)
        print("----------------------------------------------")
        print(novelty_list)

        return novelty_value



