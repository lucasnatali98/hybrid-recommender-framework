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


class AbstractMultiObjectiveRecommender(Recommender):

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
        raise NotImplementedError

    @abstractmethod
    def predict(self, pairs, ratings=None):
        """
        Calcular previsões para pares Usuário-Item

        @param pairs: Pares (Usuário-Item) -> colunas: 'user' e 'item'
        @param ratings: Dados das avaliações (Usuário-Item)
        @return: Scores que foram preditos para cada par usuário-item
        """

        raise NotImplementedError

    @abstractmethod
    def predict_for_user(self, user, items, ratings):
        """
        Calcula previsões para um usuário e itens.

        @param user: Identificador do usuário
        @param items: Itens para serem preditos (Array)
        @param ratings: Avaliações dos usuários (indexadas pelo id do item)
        @return: Os scores para os itens
        """
        raise NotImplementedError

    @abstractmethod
    def multiobjective_search(self, data=None, top_n=None, metrics=None):
        """
        Realizar otimização multiobjetivo.

        @param data: Dados necessários para a otimização
        @param top_n: Número de soluções a serem consideradas como melhores, para cada objetivo
        @param metrics: Métricas a serem otimizadas
        """
        raise NotImplementedError

    @abstractmethod
    def fitness_evaluation(self, population=None, data=None, top_n=None, metrics=None):
        """
        Realizar avaliação de fitness para a população fornecida.

        @param population: População de soluções a serem avaliadas
        @param data: Dados necessários para a otimização
        @param top_n: Número de soluções a serem consideradas como melhores, para cada objetivo
        @param metrics: Métricas a serem otimizadas
        """
        raise NotImplementedError

    @abstractmethod
    def decide_best_solution(self, X=None, F=None, weights=None):
        """
        Decidir a melhor solução com base nos critérios especificados.

        @param X: Conjunto de soluções
        @param F: Resultado dos objetivos associados a cada solução
        @param weights: Pesos a serem aplicados aos objetivos na decisão
        """
        raise NotImplementedError

