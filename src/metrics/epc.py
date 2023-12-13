from src.metrics.metric import NoveltyMetric
import pandas as pd
import numpy as np
import math


class NOVELTY(NoveltyMetric):
    """
    Abstract class representing a novelty metric.
    """

    def evaluate(self, predictions: pd.Series, features: pd.Series, **kwargs):
        raise NotImplementedError

    def get_rel_item(self, item, observed_items):
        return int(item in observed_items)

    def logarithmic_ranking_discount(self, rank):
        return 1 / math.log(rank + 2) * math.log(2)

    def reciprocal_discount(self, rank):
        return 1 / (rank + 1.0)


class EPC(NOVELTY):
    def __init__(self, cutoff):
        self.cutoff = cutoff

    @staticmethod
    def name():
        return "EPC"

    def calculate_epc(self, rec_lists, observed_items):
        item_count = {}

        for user_list in rec_lists:
            for item in user_list:
                item_count[item] = item_count.get(item, 0) + 1
                '''
                item_count é um dicionário que conta a frequência que cada item aparece na lista de recomendação
                item_count.get(item, 0): Isso verifica se o item já está presente como chave no dicionário item_count. Se estiver, item_count.get(item, 0) retornará 
                o valor associado a essa chave (ou seja, a contagem atual desse item). Se o item não estiver no dicionário, item_count.get(item, 0) retornará 0 
                (o segundo argumento é o valor padrão retornado caso a chave não exista).
                + 1: Adiciona 1 à contagem do item. Se o item já estava no dicionário, incrementa a contagem existente em 1. Se não estava, define a contagem como 1.
                
                item_count
                {40491: 402, 3567: 222, 2314: 224, 156605: 382, 5490: 466,...}
                '''

        print("item_count")
        print(item_count)

        num_users = len(rec_lists)
        item_novelty_dict = {item: 1 - (count / num_users) for item, count in item_count.items()}
        '''
        item_count.items(): Isso retorna um iterável contendo tuplas de chave-valor do dicionário item_count. Cada tupla contém um item (chave) e sua contagem (valor).

        for item, count in item_count.items(): Isso itera por cada item e sua contagem no dicionário item_count.
        
        1 - (count / num_users): Essa é a parte principal. Aqui, para cada item encontrado nas listas de recomendações, está sendo calculada a novidade (ou inverso da popularidade) desse item.
        
        count / num_users: Divide a contagem do item pelo número total de usuários (num_users). Isso resulta em uma medida normalizada da popularidade do item entre os usuários. Quanto maior a proporção, menos "novo" ou mais popular é o item entre os usuários.
        
        1 - (count / num_users): Isso calcula o inverso dessa medida. Assim, quanto menor a proporção, mais "novo" ou menos popular é o item entre os usuários.
        
        {item: 1 - (count / num_users) for item, count in item_count.items()}: Finalmente, esse dicionário compreensivo constrói um novo dicionário chamado item_novelty_dict. Em cada iteração, o item é usado como chave e o resultado de 1 - (count / num_users) (novidade do item) é atribuído como valor correspondente no novo dicionário.
        
        Em resumo, item_novelty_dict é um dicionário onde as chaves são os itens presentes nas listas de recomendações e os valores são uma medida de novidade (ou inverso da popularidade) desses itens, calculada com base na proporção de usuários que receberam essas recomendações em relação ao número total de usuários.
        
        '''
        print("item_novelty_dict")
        print(item_novelty_dict)
        print("------------------------")
        print(enumerate(rec_lists))

        epc_scores = []

        for i, user_list in enumerate(rec_lists):
            observed = observed_items.get(i + 1, [])  # i+1 corresponds to user ID starting from 1
            nov = 0
            norm = 0
            '''print("observed")
            print(observed)
            print("------------------------")
            print(i)
            print("------------------------")'''
            first_element = next(iter(observed_items.items()))

            #print(first_element)
            #print("------------------------")
            #print(self.cutoff)
            for r, item in enumerate(user_list[:self.cutoff]):
                '''print("item")
                print(item)
                print("observed")
                print(observed)'''
                rel = self.get_rel_item(item, observed)  # Get relevance of item for the user
                if rel == 1:
                    print("R")
                    print(rel)
                #discount = self.logarithmic_ranking_discount(r)  # Calculate logarithmic discount
                discount = self.reciprocal_discount(r)

                nov += rel * discount * item_novelty_dict.get(item, 1)
                norm += discount

            if norm > 0:
                nov /= norm

            epc_scores.append(nov)

        return np.mean(epc_scores)

    def evaluate(self, predictions: pd.Series, features: pd.Series, **kwargs):
        rec_lists = {}
        for user, item, _, _ in predictions.itertuples(index=False):
            if user not in rec_lists:
                rec_lists[user] = []
            if not pd.isnull(item) and pd.notnull(pd.to_numeric(item, errors='coerce')):
                rec_lists[user].append(int(item))

        rec_lists = [rec_lists[user] for user in rec_lists if rec_lists[user]]

        # Processing features DataFrame to create observed_items
        observed_items = {}
        for row in features.itertuples(index=False):
            print("row")
            print(row)
            user_id, item_id = row[0], row[1]
            if user_id not in observed_items:
                observed_items[user_id] = []
            observed_items[user_id].append(item_id)
        print("obserde itens")
        print(observed_items)
        epc_score = self.calculate_epc(rec_lists, observed_items)
        return epc_score

