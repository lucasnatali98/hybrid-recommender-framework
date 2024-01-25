from src.metrics.metric import NoveltyMetric
import pandas as pd
import numpy as np
import math
from sklearn.metrics import ndcg_score


class NOVELTY(NoveltyMetric):
    """
    Abstract class representing a novelty metric.
    """

    def evaluate(self, predictions: pd.Series, features: pd.Series, **kwargs):
        raise NotImplementedError

    # ALTERAR METODO DE RELEVÂNCIA PARA CONSIDERAR UM VALOR MINIMO DE RATING PARA CONSIDERAR RELEVANTE
    def get_relevance_item(self, item, observed_items):
        return int(item in observed_items)

    def no_relevance(self):
        return 1;

    def reciprocal_discount(self, position_recommendation):  #
        return 1 / (position_recommendation + 1.0)

def generate_item_frequency_dict(ratings_df):
    item_frequency_dict = {}
    unique_users = set()

    for index, row in ratings_df.iterrows():
        item = int(row['item'])
        user = row['user']
        item_frequency_dict[item] = item_frequency_dict.get(item, 0) + 1
        unique_users.add(user)

    num_users = len(unique_users)
    return item_frequency_dict, num_users

class EPC(NOVELTY):
    def __init__(self, cutoff, preferences_dict=None, num_users_with_preference=None):
        self.cutoff = cutoff
        self.item_frequency_dict = preferences_dict
        self.num_users = num_users_with_preference

    def calculate_epc(self, rec_lists, ratings_df):
        if self.item_frequency_dict is None or self.num_users is None:
            self.item_frequency_dict, self.num_users = generate_item_frequency_dict(ratings_df)
            print("Número de usuários únicos:", self.num_users)
            print("Dicionário de frequência para itens:", self.item_frequency_dict)

        item_novelty_dict = {item: 1 - (frequency / self.num_users) for item, frequency in self.item_frequency_dict.items()}

        epc_scores = []
        for index_rec_list, rec_list in enumerate(rec_lists):
            epc_score = 0
            norm = 0

            for index_item, item in enumerate(rec_list[:self.cutoff]):  # percorre os items que foram recomendados
                relevance = self.no_relevance()
                discount = self.reciprocal_discount(index_item)  # desconto associado a posição do item na lista de recomendação, descontos mais altos para items em pos mais alta

                epc_score += discount * relevance * item_novelty_dict.get(item, 1)
                norm += discount
                '''print("epc")
                print(epc_score)
                print(discount)
                print(relevance)
                print(item_novelty_dict.get(item, 1))
                print("norm")
                print(norm)'''
            if norm > 0:
                epc_score /= norm

            epc_scores.append(epc_score)

        return np.mean(epc_scores)

    def evaluate(self, predictions: pd.Series, features: pd.Series, **kwargs):  # recommendations_df, df_all_ratings
        rec_lists = {}
        # Transforma as predictions em um objeto {1:[12,15,20], 2:[1,2,3]}
        for user, item, _, _ in predictions.itertuples(index=False):
            if user not in rec_lists:
                rec_lists[user] = []
            if not pd.isnull(item) and pd.notnull(pd.to_numeric(item, errors='coerce')):
                rec_lists[user].append(int(item))

        rec_lists = [rec_lists[user] for user in rec_lists if rec_lists[user]]

        ratings_df = features
        epc_score = self.calculate_epc(rec_lists, ratings_df)
        return epc_score

