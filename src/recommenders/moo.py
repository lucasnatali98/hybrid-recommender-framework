from src.recommenders.recommender import AbstractMultiObjectiveRecommender
import pandas as pd
import numpy as np

import os
import json

from src.metrics.epc import EPC
from src.metrics.epc import generate_item_frequency_dict
from src.metrics.ndcg import SklearnNDCG

import heapq

from src.utils import process_parameters

from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.util.ref_dirs import get_reference_directions

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.age import AGEMOEA
from pymoo.decomposition.asf import ASF
from pymoo.operators.mutation.pm import PolynomialMutation
from pymoo.operators.crossover.ux import UniformCrossover
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.gauss import GM
from pymoo.termination import get_termination
from pymoo.indicators.hv import Hypervolume

from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM


from pymoo.visualization.scatter import Scatter
import matplotlib.pyplot as plt
from pymoo.util.plotting import plot


from sklearn.metrics import ndcg_score


class MOO(AbstractMultiObjectiveRecommender):
    """
    """
    def recommend(self, users, n, candidates=None, ratings=None, **kwargs):
        raise NotImplementedError

    def predict(self, pairs, ratings):
        raise NotImplementedError

    def predict_for_user(self, user, items, ratings):
        raise NotImplementedError

    def fit(self, rating, **kwargs) -> None:
        raise NotImplementedError

    def get_params(self, deep=True):
        raise NotImplementedError

    def multiobjective_search(self, data=None, top_n=None, metrics=None):
        raise NotImplementedError

    def fitness_evaluation(self, population=None, data=None, top_n=None, metrics=None):
        raise NotImplementedError

    def decide_best_solution(self, X, F, weights, file_path_save_solution=None, file_name_best_solution=None, file_name_best_solution_result=None, method='compromise_programming', custom_decision_function=None):
        F = np.array(F)
        if method == 'compromise_programming':
            decomp = ASF()
            index = decomp(F, weights).argmin()
        elif method == 'weighted_sum':
            values = np.dot(F, weights)
            index = np.argmax(values)
        elif callable(custom_decision_function):
            index = custom_decision_function(F)
        else:
            raise ValueError("Método de decisão inválido.")

        if file_path_save_solution and file_name_best_solution and file_name_best_solution_result:
            file_path_best_solution = os.path.join(file_path_save_solution, file_name_best_solution)
            file_path_best_solution_result = os.path.join(file_path_save_solution, file_name_best_solution_result)

            with open(file_path_best_solution, 'w') as file:
                json.dump(X[index].tolist(), file)

            with open(file_path_best_solution_result, 'w') as file:
                json.dump(F[index].tolist(), file)

        return X[index], index

def create_user_dataframes(user, scores_list):
    """
       Cria DataFrames contendo as recomendações e os ratings para um usuário específico.

       Parâmetros:
           user (int): O ID do usuário para o qual as recomendações e ratings serão criados.
           scores_list (list): Uma lista contendo tuplas no formato (item, score, rating).

       Retorna:
           tuple: Uma tupla contendo dois DataFrames, um para as recomendações e outro para os ratings.
    """
    recommendations_df = pd.DataFrame(columns=['user', 'item', 'score', 'algorithm_name'])
    ratings_df = pd.DataFrame(columns=['user', 'item', 'rating'])

    for item, score, rating in scores_list:
        recommendations_df = pd.concat([recommendations_df, pd.DataFrame({'user': [user], 'item': [item], 'score': [score], 'algorithm_name': ['nsga2']})], ignore_index=True)
        ratings_df = pd.concat([ratings_df, pd.DataFrame({'user': [user], 'item': [item], 'rating': [rating]})], ignore_index=True)

    return recommendations_df, ratings_df

def get_top_n_score(features_in_memory_dict, weights, top_n):
    """
     Calcula os scores normalizados das features e retorna as melhores recomendações para cada usuário.

     Parâmetros:
         features_in_memory_dict (dict): Um dicionário onde as chaves são strings no formato 'usuario,item' e os valores são dicionários contendo as features e o rating do item.
         weights (list): Uma lista de pesos para as features.
         top_n (int): O número de recomendações desejadas para cada usuário.

     Retorna:
         dict: Um dicionário onde as chaves são os IDs dos usuários e os valores são listas de tuplas no formato (item, score, rating) representando as melhores recomendações para cada usuário.
     """

    scores = {}
    for usuario_item, data in features_in_memory_dict.items():
        features = data['features']
        rating = data['rating']

        score_sum = sum(weights[feature - 1] * value for feature, value in features.items())
        num_features = len(features)
        normalized_score_sum = score_sum / num_features
        scores[usuario_item] = (rating, normalized_score_sum)

    topn_scores = {}
    for usuario_item, (rating, score) in scores.items():
        usuario, item = map(int, usuario_item.split(','))
        if usuario not in topn_scores:
            topn_scores[usuario] = []
        topn_scores[usuario].append((item, score, rating)) #(item, score, rating)

    for usuario, scores_list in topn_scores.items():
        topn_scores[usuario] = heapq.nlargest(top_n, scores_list, key=lambda x: x[1])

    return topn_scores
    #topn_scores {1002: [(296, 5.694619656291464, 1.0), (2858, 5.598729910716902, 1.0)

def get_all_ratings(features_in_memory_dict):
    """
    Obtém todos os ratings de itens do conjunto de dados.

    Parâmetros:
        features_in_memory_dict (dict): Um dicionário onde as chaves são strings no formato 'usuario,item' e os valores são dicionários contendo as features e o rating do item.

    Retorna:
        list: Uma lista de tuplas no formato (usuario, item, rating) representando todos os ratings de itens no conjunto de dados.
    """
    all_ratings = []
    for usuario_item, data in features_in_memory_dict.items():
        rating = data['rating']
        all_ratings.append((int(usuario_item.split(',')[0]), int(usuario_item.split(',')[1]), rating))
    return all_ratings

class FitnessEvaluation(Problem):
    def __init__(self, num_features, top_n, features_in_memory_dict, metrics=None, metric_params=None):
        """
        Inicializa a classe de avaliação de fitness do problema.

        Parâmetros:
            num_features (int): O número de características (ou dimensões) do problema.
            top_n (int): O número de itens principais a serem recomendados para cada usuário.
            features_in_memory_dict (dict): Um dicionário onde as chaves são strings no formato 'usuario,item' e os valores são dicionários contendo as características e o rating do item.
            metrics (list): Uma lista de classes de métricas a serem usadas na avaliação do fitness. Se não for fornecida, uma lista vazia será usada.
            metric_params (dict): Um dicionário contendo parâmetros adicionais para as métricas, onde as chaves são as classes de métricas e os valores são os parâmetros específicos de cada métrica.
        """

        super().__init__(n_var=num_features, n_obj=len(metrics), n_constr=0, xl=0, xu=1)

        self.top_n = top_n
        self.features_in_memory_dict = features_in_memory_dict
        self.metrics = metrics or []
        self.metric_params = metric_params or {}
    def _evaluate(self, population, out, *args, **kwargs):
        """
            Avalia o fitness da população de soluções.

            Parâmetros:
                population (numpy.ndarray): A população de soluções a ser avaliada.
                out (dict): Um dicionário de saída contendo as informações do fitness avaliado.
        """
        top_n = self.top_n
        features_in_memory_dict = self.features_in_memory_dict
        metrics = self.metrics
        metric_params = self.metric_params

        objective_values = []

        all_ratings = get_all_ratings(features_in_memory_dict)
        df_all_ratings = pd.DataFrame(all_ratings, columns=['user', 'item', 'rating'])

        for solution in population:
            weights = solution
            topn_scores = get_top_n_score(features_in_memory_dict, weights, top_n)

            user_metric_values = []
            for user, scores_list in topn_scores.items():
                recommendations_user_df, ratings_user_df = create_user_dataframes(user, scores_list)

                user_metrics = []
                for metric_class in metrics:
                    metric_instance = metric_class(**metric_params.get(metric_class, {}))
                    metric_value = metric_instance.evaluate(recommendations_user_df, df_all_ratings)
                    user_metrics.append(-metric_value)  #maximize

                user_metric_values.append(user_metrics)

            user_avg_metrics = np.array(user_metric_values).mean(axis=0)
            objective_values.append(user_avg_metrics)

        out["F"] = np.array(objective_values)

class NSGA2PyMoo(MOO):
    def __init__(self, pop_size, top_n, num_features, termination_type="n_gen", termination_value=1, mutation=GM(), crossover=TwoPointCrossover(prob=0.9), seed=None, experiment=None, fitness_evaluator=None):
        """
            Inicializa o algoritmo NSGA-II para otimização multiobjetivo.

            Parâmetros:
                pop_size (int): Tamanho da população.
                top_n (int): Número de itens principais a serem recomendados para cada usuário.
                num_features (int): Número de características (ou dimensões) do problema.
                termination_type (str): Tipo de critério de término da otimização (exemplo: "n_gen" para número de gerações e "time" para tempo de execução do experimento).
                termination_value (int): Valor do critério de término (exemplo: 10, para "n_gen" ou "00:30:00" para "time").
                mutation (Mutation): Operador de mutação a ser utilizado.
                crossover (Crossover): Operador de crossover a ser utilizado.
                seed (int): Semente para reprodução de resultados.
                experiment (int): Número do experimento para salvar no arquivo.
                fitness_evaluator (FitnessEvaluation): Avaliador de fitness a ser utilizado.
        """
        self.pop_size = pop_size
        self.seed = seed
        self.top_n = top_n
        self.num_features = num_features
        self.mutation = mutation
        self.crossover = crossover
        self.termination_type = termination_type
        self.termination_value = termination_value
        self.experiment = experiment
        self.fitness_evaluator = fitness_evaluator

    def multiobjective_search(self, features_in_memory_dict, metrics=None, metric_params=None, folder_path=None, **kwargs):
        """
            Executa a busca multiobjetivo usando o algoritmo NSGA-II.

            Parâmetros:
                features_in_memory_dict (dict): Um dicionário onde as chaves são strings no formato 'usuario,item' e os valores são dicionários contendo as características e o rating do item.
                metrics (list): Uma lista de classes de métricas a serem usadas na avaliação do fitness.
                metric_params (dict): Um dicionário contendo parâmetros adicionais para as métricas.
                folder_path (str): Caminho para o diretório onde os resultados serão salvos.

            Retorna:
                X: Matriz de soluções do NSGA-II.
                F: Matriz de valores objetivos (fitness) associados às soluções do NSGA-II.
        """
        pop_size = self.pop_size
        seed = self.seed
        top_n = self.top_n
        num_features = self.num_features
        mutation = self.mutation
        crossover = self.crossover
        termination_type = self.termination_type
        termination_value = self.termination_value
        experiment = self.experiment

        if self.fitness_evaluator is None:
            self.fitness_evaluator = FitnessEvaluation(num_features, top_n, features_in_memory_dict, metrics, metric_params)

        problem = self.fitness_evaluator
        algorithm = NSGA2(pop_size=pop_size, mutation=mutation, crossover=crossover)
        termination = get_termination(termination_type, termination_value)
        optimization_result = minimize(problem, algorithm, termination, seed, save_history=True, verbose=True)

        X = optimization_result.X
        F = optimization_result.F

        F = -F

        if folder_path:
            file_name_X = f'experiment_{experiment}_pareto_front.json'
            file_name_F = f'experiment_{experiment}_pareto_front_objectives_results.json'

            file_path_X = os.path.join(folder_path, file_name_X)
            file_path_F = os.path.join(folder_path, file_name_F)
            os.makedirs(folder_path, exist_ok=True)

            with open(file_path_X, 'w') as file:
                json.dump(X.tolist(), file)

            with open(file_path_F, 'w') as file:
                json.dump(F.tolist(), file)

            #plot.save(os.path.join(folder_path, f'experiment_{experiment}_nsga2_pareto.png'))

        return X, F

    def recommend(self, features_in_memory_dict, solution, top_n, folder_path=None, file_name_test_prediction=None):
        topn_scores = get_top_n_score(features_in_memory_dict, solution, top_n)

        if folder_path and file_name_test_prediction:
            file_path_predict = os.path.join(folder_path, file_name_test_prediction)
            os.makedirs(folder_path, exist_ok=True)

            with open(file_path_predict, 'w') as json_file:
                json.dump(topn_scores, json_file)
        return topn_scores
    def predict_for_user(self, user, features_in_memory_dict, solution, top_n, folder_path=None, file_name_test_prediction=None):
        topn_scores = get_top_n_score(features_in_memory_dict, solution, top_n)

        if folder_path and file_name_test_prediction:
            file_path_predict = os.path.join(folder_path, file_name_test_prediction)
            os.makedirs(folder_path, exist_ok=True)

            with open(file_path_predict, 'w') as json_file:
                json.dump(topn_scores[user], json_file)
        return topn_scores[user]


class AGEMOEAPyMoo(MOO):
    def __init__(self, pop_size, top_n, num_features, termination_type="n_gen", termination_value=1, mutation=GM(), crossover=TwoPointCrossover(prob=0.9), seed=None, experiment=None, fitness_evaluator=None):
        """
            Inicializa o algoritmo NSGA-II para otimização multiobjetivo.

            Parâmetros:
                pop_size (int): Tamanho da população.
                top_n (int): Número de itens principais a serem recomendados para cada usuário.
                num_features (int): Número de características (ou dimensões) do problema.
                termination_type (str): Tipo de critério de término da otimização (exemplo: "n_gen" para número de gerações e "time" para tempo de execução do experimento).
                termination_value (int): Valor do critério de término (exemplo: 10, para "n_gen" ou "00:30:00" para "time").
                mutation (Mutation): Operador de mutação a ser utilizado.
                crossover (Crossover): Operador de crossover a ser utilizado.
                seed (int): Semente para reprodução de resultados.
                experiment (int): Número do experimento para salvar no arquivo.
                fitness_evaluator (FitnessEvaluation): Avaliador de fitness a ser utilizado.
        """
        self.pop_size = pop_size
        self.seed = seed
        self.top_n = top_n
        self.num_features = num_features
        self.mutation = mutation
        self.crossover = crossover
        self.termination_type = termination_type
        self.termination_value = termination_value
        self.experiment = experiment
        self.fitness_evaluator = fitness_evaluator

    def multiobjective_search(self, features_in_memory_dict, metrics=None, metric_params=None, folder_path=None, **kwargs):
        """
            Executa a busca multiobjetivo usando o algoritmo NSGA-II.

            Parâmetros:
                features_in_memory_dict (dict): Um dicionário onde as chaves são strings no formato 'usuario,item' e os valores são dicionários contendo as características e o rating do item.
                metrics (list): Uma lista de classes de métricas a serem usadas na avaliação do fitness.
                metric_params (dict): Um dicionário contendo parâmetros adicionais para as métricas.
                folder_path (str): Caminho para o diretório onde os resultados serão salvos.

            Retorna:
                X: Matriz de soluções do NSGA-II.
                F: Matriz de valores objetivos (fitness) associados às soluções do NSGA-II.
        """
        pop_size = self.pop_size
        seed = self.seed
        top_n = self.top_n
        num_features = self.num_features
        mutation = self.mutation
        crossover = self.crossover
        termination_type = self.termination_type
        termination_value = self.termination_value
        experiment = self.experiment

        if self.fitness_evaluator is None:
            self.fitness_evaluator = FitnessEvaluation(num_features, top_n, features_in_memory_dict, metrics, metric_params)

        problem = self.fitness_evaluator
        algorithm = AGEMOEA(pop_size=pop_size, mutation=mutation, crossover=crossover)
        termination = get_termination(termination_type, termination_value)
        optimization_result = minimize(problem, algorithm, termination, seed, save_history=True, verbose=True)

        X = optimization_result.X
        F = optimization_result.F

        F = -F

        if folder_path:
            file_name_X = f'experiment_{experiment}_pareto_front.json'
            file_name_F = f'experiment_{experiment}_pareto_front_objectives_results.json'

            file_path_X = os.path.join(folder_path, file_name_X)
            file_path_F = os.path.join(folder_path, file_name_F)
            os.makedirs(folder_path, exist_ok=True)

            with open(file_path_X, 'w') as file:
                json.dump(X.tolist(), file)

            with open(file_path_F, 'w') as file:
                json.dump(F.tolist(), file)


        return X, F

    def recommend(self, features_in_memory_dict, weights, top_n, folder_path=None, file_name_test_prediction=None):
        topn_scores = get_top_n_score(features_in_memory_dict, weights, top_n)

        if folder_path and file_name_test_prediction:
            file_path_predict = os.path.join(folder_path, file_name_test_prediction)
            os.makedirs(folder_path, exist_ok=True)

            with open(file_path_predict, 'w') as json_file:
                json.dump(topn_scores, json_file)
        return topn_scores

    def predict_for_user(self, user, features_in_memory_dict, weights, top_n, folder_path=None, file_name_test_prediction=None):
        topn_scores = get_top_n_score(features_in_memory_dict, weights, top_n)

        if folder_path and file_name_test_prediction:
            file_path_predict = os.path.join(folder_path, file_name_test_prediction)
            os.makedirs(folder_path, exist_ok=True)

            with open(file_path_predict, 'w') as json_file:
                json.dump(topn_scores[user], json_file)
        return topn_scores[user]