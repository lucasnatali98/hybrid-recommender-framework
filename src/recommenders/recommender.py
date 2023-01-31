from abc import abstractmethod
import pandas as pd
from src.recommenders.algorithm import Algorithm


class Recommender(Algorithm):
    @abstractmethod
    def recommend(self, users, n, candidates=None, ratings=None) -> pd.DataFrame:
        """
        Calcular recomendações para um usuário.

        @param users: Conjunto de usuários
        @param n: Número de recomendações que serão produzidas
        @param candidates: Conjunto de itens candidados
        @param ratings: as avaliações dos usuŕios (indexados pelo id do item)
        @return:
        """
        pass

    @abstractmethod
    def predict(self, pairs, ratings):
        """
        Calcular previsões para pares Usuário-Item

        @param pairs: Pares (Usuário-Item) -> colunas: 'user' e 'item'
        @param ratings: Dados das avaliações (Usuário-Item)
        @return: Scores que foram preditos para cada par usuário-item
        """

        pass

    @abstractmethod
    def predict_for_user(self, user, items, ratings):
        """
        Calcula previsões para um usuário e itens.

        @param user: Identificador do usuário
        @param items: Itens para serem preditos (Array)
        @param ratings: Avaliações dos usuários (indexadas pelo id do item)
        @return: Os scores para os itens
        """
        pass
