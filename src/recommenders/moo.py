from src.recommenders.recommender import AbstractMultiObjectiveRecommender
import pandas as pd
import numpy as np

import os
import json

from src.metrics.epc import EPC
from src.metrics.epc import generate_item_frequency_dict
from src.metrics.ndcg import LenskitNDCG


import heapq



from src.utils import process_parameters

from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.util.ref_dirs import get_reference_directions

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.age import AGEMOEA
from pymoo.mcdm.pseudo_weights import PseudoWeights
from pymoo.decomposition.asf import ASF

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

def create_user_dataframes(user, scores_list):
    recommendations_df = pd.DataFrame(columns=['user', 'item', 'score', 'algorithm_name'])

    for item, score, rating in scores_list:
        recommendations_df = pd.concat([recommendations_df, pd.DataFrame({'user': [user], 'item': [item], 'score': [score], 'algorithm_name': ['nsga2']})], ignore_index=True)

    return recommendations_df

# Função para calcular métricas para um usuário específico
def get_top_n_score(features_in_memory_dict, weights, top_n):
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
    all_ratings = []
    for usuario_item, data in features_in_memory_dict.items():
        rating = data['rating']
        all_ratings.append((int(usuario_item.split(',')[0]), int(usuario_item.split(',')[1]), rating))
    return all_ratings


class FitnessEvaluation(Problem):
    def __init__(self, num_features, top_n, features_in_memory_dict):
        super().__init__(n_var=num_features, n_obj=2, n_constr=0, xl=0, xu=1)

        self.top_n = top_n
        self.features_in_memory_dict = features_in_memory_dict
    def _evaluate(self, population, out, *args, **kwargs):
        '''print("população----------------------------")
        print(population)'''
        top_n = self.top_n
        features_in_memory_dict = self.features_in_memory_dict
        objective_values = []

        all_ratings = get_all_ratings(features_in_memory_dict)
        df_all_ratings = pd.DataFrame(all_ratings, columns=['user', 'item', 'rating'])
        preferences_dict, num_users_with_preference = generate_item_frequency_dict(ratings_df=df_all_ratings)

        #Percorro cada solução da população que seria um conjunto de pesos para aplicar nas features dos pares usuario x item do arquivo
        for solution in population:
            weights = solution
            #passo os pesos, o arquivo e o tamanho do top_n para a função que vai processar esses arquivos e voltar com
            # o topn_scores {user: [(item, score, rating)]
            topn_scores = get_top_n_score(features_in_memory_dict, weights, top_n)

            novelty_scores = []
            accuracy_scores = []

            for user, scores_list in topn_scores.items():
                recommendations_user_df = create_user_dataframes(user, scores_list)

                epc = EPC(cutoff=top_n, preferences_dict=preferences_dict, num_users_with_preference=num_users_with_preference)
                items, scores, ratings = zip(*scores_list)
                ratings = np.array([ratings])  # Convertendo para uma matriz bidimensional
                scores = np.array([scores])

                novelty = epc.evaluate(recommendations_user_df, df_all_ratings)
                accuracy = ndcg_score(ratings, scores, k=top_n)

                print("acuracy----------------")
                print(accuracy)
                print("novelty------------------")
                print(novelty)

                novelty_scores.append(-novelty)
                accuracy_scores.append(-accuracy)

            # Calcular média das métricas
            avg_novelty = sum(novelty_scores) / len(novelty_scores)
            avg_accuracy = sum(accuracy_scores) / len(accuracy_scores)
            #Salvo a média das métricas para cada solução
            objective_values.append(avg_accuracy)
            objective_values.append(avg_novelty)

        out["F"] = np.array(objective_values)

def decide_best_solution(X, F, weights, algorithm):
    #Compromise Programming
    F = np.array(F)
    decomp = ASF()
    index = decomp(F, weights).argmax()

    relative_path = f'PycharmProjects/RecSysExp/experiment_output/moo/{algorithm}'
    file_name_best_solution = 'best_solution.json'
    folder_path = os.path.expanduser(f'~/{relative_path}')
    file_path_best_solution = os.path.join(folder_path, file_name_best_solution)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_best_solution, 'w') as file:
        json.dump(X[index], file)

    return X[index]


class NSGA2PyMoo(MOO):
    def __init__(self, pop_size, n_gen, top_n, num_features, seed=None):
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.seed = seed
        self.top_n = top_n
        self.num_features = num_features

    def recommend(self, features_in_memory_dict, **kwargs):
        pop_size = self.pop_size
        n_gen = self.n_gen
        seed = self.seed
        top_n = self.top_n
        num_features = self.num_features

        problem = FitnessEvaluation(num_features, top_n, features_in_memory_dict)
        algorithm = NSGA2(pop_size=pop_size)
        termination = ("n_gen", n_gen)
        optimization_result = minimize(problem, algorithm, termination, seed)#Trocar por maximizar?

        X = optimization_result.X
        F = -optimization_result.F

        relative_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2'
        file_name_X = 'pareto_front.json'
        file_name_F = 'results_solutions.json'

        folder_path = os.path.expanduser(f'~/{relative_path}')
        file_path_X = os.path.join(folder_path, file_name_X)
        file_path_F = os.path.join(folder_path, file_name_F)
        os.makedirs(folder_path, exist_ok=True)

        with open(file_path_X, 'w') as file:
            json.dump(X.tolist(), file)

        with open(file_path_F, 'w') as file:
            json.dump(F.tolist(), file)

        return X, F

    def predict(self, features_in_memory_dict, weights, top_n):
        topn_scores = get_top_n_score(features_in_memory_dict, weights, top_n)

        relative_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2'
        file_name_predict = f'predict_all_users_top_{top_n}.json'
        folder_path = os.path.expanduser(f'~/{relative_path}')
        file_path_predict = os.path.join(folder_path, file_name_predict)
        os.makedirs(folder_path, exist_ok=True)

        with open(file_path_predict, 'w') as json_file:
            json.dump(topn_scores, json_file)
        return topn_scores
    def predict_for_user(self, user, features_in_memory_dict, weights, top_n):
        topn_scores = get_top_n_score(features_in_memory_dict, weights, top_n)

        relative_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2'
        file_name_predict = f'predict_to_user_{user}_top_{top_n}.json'
        folder_path = os.path.expanduser(f'~/{relative_path}')
        file_path_predict = os.path.join(folder_path, file_name_predict)
        os.makedirs(folder_path, exist_ok=True)

        with open(file_path_predict, 'w') as json_file:
            json.dump(topn_scores[user], json_file)
        return topn_scores[user]

class NSGA3PyMoo(MOO):

    def __init__(self, pop_size, n_gen, top_n, num_features, num_partitions, seed=None):
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.seed = seed
        self.top_n = top_n
        self.num_features = num_features
        self.num_partitions = num_partitions

    def recommend(self, features_in_memory_dict, **kwargs):
        pop_size = self.pop_size
        n_gen = self.n_gen
        num_partitions = self.num_partitions
        seed = self.seed
        top_n = self.top_n
        num_features = self.num_features
        num_objectives = 2

        ref_dirs = get_reference_directions("uniform", num_objectives, n_partitions=num_partitions)
        problem = FitnessEvaluation(num_features, top_n, features_in_memory_dict)
        algorithm = NSGA3(pop_size=pop_size,ref_dirs=ref_dirs)
        termination = ("n_gen", n_gen)
        optimization_result = minimize(problem, algorithm, termination, seed)

        X = optimization_result.X
        F = -optimization_result.F

        relative_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga3'
        file_name_X = 'pareto_front.json'
        file_name_F = 'results_solutions.json'

        folder_path = os.path.expanduser(f'~/{relative_path}')
        file_path_X = os.path.join(folder_path, file_name_X)
        file_path_F = os.path.join(folder_path, file_name_F)
        os.makedirs(folder_path, exist_ok=True)

        with open(file_path_X, 'w') as file:
            json.dump(X.tolist(), file)

        with open(file_path_F, 'w') as file:
            json.dump(F.tolist(), file)

        return X, F

    def predict(self, features_in_memory_dict, weights, top_n):
        topn_scores = get_top_n_score(features_in_memory_dict, weights, top_n)

        relative_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga3'
        file_name_predict = f'predict_all_users_top_{top_n}.json'
        folder_path = os.path.expanduser(f'~/{relative_path}')
        file_path_predict = os.path.join(folder_path, file_name_predict)
        os.makedirs(folder_path, exist_ok=True)

        with open(file_path_predict, 'w') as json_file:
            json.dump(topn_scores, json_file)
        return topn_scores

    def predict_for_user(self, user, features_in_memory_dict, weights, top_n):
        topn_scores = get_top_n_score(features_in_memory_dict, weights, top_n)

        relative_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga3'
        file_name_predict = f'predict_to_user_{user}_top_{top_n}.json'
        folder_path = os.path.expanduser(f'~/{relative_path}')
        file_path_predict = os.path.join(folder_path, file_name_predict)
        os.makedirs(folder_path, exist_ok=True)

        with open(file_path_predict, 'w') as json_file:
            json.dump(topn_scores[user], json_file)
        return topn_scores[user]

class AGEMOEAPyMoo(MOO):
    def __init__(self, pop_size, n_gen, top_n, num_features, seed=None):
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.seed = seed
        self.top_n = top_n
        self.num_features = num_features

    def recommend(self, features_in_memory_dict, **kwargs):
        pop_size = self.pop_size
        n_gen = self.n_gen
        seed = self.seed
        top_n = self.top_n
        num_features = self.num_features

        problem = FitnessEvaluation(num_features, top_n, features_in_memory_dict)
        algorithm = AGEMOEA(pop_size=pop_size)
        termination = ("n_gen", n_gen)
        optimization_result = minimize(problem, algorithm, termination, seed)

        X = optimization_result.X
        F = -optimization_result.F

        relative_path = 'PycharmProjects/RecSysExp/experiment_output/moo/agemoea'
        file_name_X = 'pareto_front.json'
        file_name_F = 'results_solutions.json'

        folder_path = os.path.expanduser(f'~/{relative_path}')
        file_path_X = os.path.join(folder_path, file_name_X)
        file_path_F = os.path.join(folder_path, file_name_F)
        os.makedirs(folder_path, exist_ok=True)

        # Save the file to the specified path
        with open(file_path_X, 'w') as file:
            json.dump(X.tolist(), file)

        with open(file_path_F, 'w') as file:
            json.dump(F.tolist(), file)

        return X, F

    def predict(self, features_in_memory_dict, weights, top_n):
        topn_scores = get_top_n_score(features_in_memory_dict, weights, top_n)

        relative_path = 'PycharmProjects/RecSysExp/experiment_output/moo/agemoea'
        file_name_predict = f'predict_all_users_top_{top_n}.json'
        folder_path = os.path.expanduser(f'~/{relative_path}')
        file_path_predict = os.path.join(folder_path, file_name_predict)
        os.makedirs(folder_path, exist_ok=True)

        with open(file_path_predict, 'w') as json_file:
            json.dump(topn_scores, json_file)
        return topn_scores

    def predict_for_user(self, user, features_in_memory_dict, weights, top_n):
        topn_scores = get_top_n_score(features_in_memory_dict, weights, top_n)

        relative_path = 'PycharmProjects/RecSysExp/experiment_output/moo/agemoea'
        file_name_predict = f'predict_to_user_{user}_top_{top_n}.json'
        folder_path = os.path.expanduser(f'~/{relative_path}')
        file_path_predict = os.path.join(folder_path, file_name_predict)
        os.makedirs(folder_path, exist_ok=True)

        with open(file_path_predict, 'w') as json_file:
            json.dump(topn_scores[user], json_file)
        return topn_scores[user]

