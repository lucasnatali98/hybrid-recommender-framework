from src.metrics.metric import DiversityMetric
from typing import List
import recmetrics
import pandas as pd

class DIVERSITY(DiversityMetric):
    """

    """
    def evaluate(self, predictions: pd.Series, features: pd.Series, **kwargs):
        raise NotImplementedError


class RecmetricsDIVERSITY(DIVERSITY):
    def evaluate(self, predictions: pd.Series, features: pd.Series, **kwargs): #recomendações e features
        # Prediction list
        rec_lists = {}
        for user, item, _, _ in predictions.itertuples(index=False):
            if user not in rec_lists:
                rec_lists[user] = []
            # Verifica se o item não é NaN e é um número
            if not pd.isnull(item) and pd.notnull(pd.to_numeric(item, errors='coerce')):
                rec_lists[user].append(int(item))  # Convert item to int

        # print('rec list 1')
        # print(rec_lists)

        # Verifica se a lista de recomendações para cada usuário não está vazia antes de adicioná-la
        rec_lists = [rec_lists[user] for user in rec_lists if rec_lists[user]]  # Remove listas vazias
        print('rec list 2')
        print(rec_lists)
        diversity = recmetrics.intra_list_similarity(rec_lists, features)
        #print("----------------------------------------------")
        #print(diversity)
        return diversity


class GiniIndexDIVERSITY(DIVERSITY):
    def evaluate(self, predictions: pd.Series, features: pd.Series, **kwargs):
        def calculate_gini(recommendations: pd.Series):
            # Contagem de recomendações por item
            item_counts = recommendations.value_counts()
            # Total de itens recomendados
            total_recommendations = len(recommendations)
            # Proporção cumulativa de usuários até cada item
            cum_prop = item_counts.cumsum() / total_recommendations
            # Posições dos itens na lista ordenada por popularidade
            ranks = pd.Series(range(1, len(item_counts) + 1), index=item_counts.index)

            # Cálculo do índice de Gini
            gini_sum = ((cum_prop.shift(fill_value=0) + cum_prop) * (ranks.diff().fillna(0))).sum()
            gini_index = 1 - gini_sum

            return gini_index

        # Extraindo apenas os itens recomendados
        recommended_items = predictions['item']

        # Calculando o índice de Gini para as recomendações
        gini_diversity = calculate_gini(recommended_items)

        return gini_diversity

