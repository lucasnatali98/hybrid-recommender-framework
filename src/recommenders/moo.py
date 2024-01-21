from src.recommenders.recommender import AbstractMultiObjectiveRecommender
import pandas as pd
import numpy as np

from src.metrics.epc import EPC
from src.metrics.diversity import RecmetricsDIVERSITY
from src.metrics.ndcg import LenskitNDCG
from src.metrics.recall import LenskitRecall
from src.metrics.gini import GiniIndex
import lenskit.metrics.topn as lenskit_topn


from src.utils import process_parameters

from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.util.ref_dirs import get_reference_directions

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.age import AGEMOEA



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
    ratings_df = pd.DataFrame(columns=['user', 'item', 'rating'])

    for item, score, rating in scores_list:
        recommendations_df = pd.concat([recommendations_df, pd.DataFrame({'user': [user], 'item': [item], 'score': [score], 'algorithm_name': ['nsga2']})], ignore_index=True)
        ratings_df = pd.concat([ratings_df, pd.DataFrame({'user': [user], 'item': [item], 'rating': [rating]})], ignore_index=True)

    return recommendations_df, ratings_df

# Função para calcular métricas para um usuário específico
def calculate_metrics(user_recommendations, user_ratings, cutoff):
    '''parameters = {
        "k": "None",
        "sample_weight": "None",
        "ignore_ties": "false"
    }'''

    parameters = {
        "labels": "None",
        "average": "binary",
        "sample_weight": "None",
        "zero_division": "warn"
    }


    recall = LenskitRecall(parameters)

    epc = EPC(cutoff)
    ndcg = LenskitNDCG(parameters)

    novelty = epc.evaluate(user_recommendations, user_ratings)
    accuracy = recall.evaluate(user_recommendations, user_ratings)

    return novelty, accuracy

def process_file(file_path, weights, top_n):
    scores = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            parts = line.strip().split('\t')
            user_item = parts[0]

            rating, *features_str = parts[1].split()
            rating = float(rating)
            features = {int(f.split(':')[0]): float(f.split(':')[1]) for f in features_str}

            num_features = len(features)

            #Calculo peso * feature
            score_sum = sum(weights[feature - 1] * value for feature, value in features.items())
            #Normalizo dividindo pelo total de features
            normalized_score_sum = score_sum / num_features
            #Para cada par usuario x item salvo o rating e o score normalizado
            scores[user_item] = (rating, normalized_score_sum)

    top_n_scores = {}
    #Percorro os scores e salvo para cada usuário  os items dele no formato (item,score,rating)
    for user_item, (rating, score) in scores.items():
        user, item = map(int, user_item.split(','))
        if user not in top_n_scores:
            top_n_scores[user] = []
        top_n_scores[user].append((item, score, rating))

    #Ordeno os que tem maior score e pego os primeiros top_n para cada usuário, usei um método de ordenação simples, depois eu vou voltar nisso
    for user, scores_list in top_n_scores.items():
        scores_list.sort(key=lambda x: x[1], reverse=True)
        top_n_scores[user] = scores_list[:top_n]

    return top_n_scores
    #topn_scores {1002: [(296, 5.694619656291464, 1.0), (2858, 5.598729910716902, 1.0)

class FitnessEvaluation(Problem):
    def __init__(self, num_features, top_n, num_items, num_users, ratings, cutoff, arquivo_path):
        super().__init__(n_var=num_features, n_obj=2, n_constr=0, xl=0, xu=1)

        self.ratings = ratings
        self.cutoff = cutoff
        self.top_n = top_n
        self.arquivo_path = arquivo_path

    def _evaluate(self, population, out, *args, **kwargs):
        print("população----------------------------")
        print(population)
        '''
        -------------------individuo-------------------
        [0.90850257 0.91387016 0.07832085 ... 0.87716883 0.80064328 0.53347508] Pesos para as features
        
        '''
        cutoff = self.cutoff
        top_n = self.top_n

        #Percorro cada solução da população que seria um conjunto de pesos para aplicar nas features dos pares usuario x item do arquivo
        for solution in population:
            weights = solution
            #passo os pesos, o arquivo e o tamanho do top_n para a função que vai processar esses arquivos e voltar com
            # o topn_scores {user: [(item, score, rating)]
            topn_scores = process_file('/home/usuario/PycharmProjects/RecSysExp/data_storage/hr/HR-all-train.merged', weights, top_n)

            res = []

            # Lista para armazenar as métricas de cada usuário
            novelty_scores = []
            accuracy_scores = []
            #Percorro o topn_scores
            for user, scores_list in topn_scores.items():
                #Para cada user transformo os dados em 2 df, um das recomendações e um dos ratings, da forma que o algoritmo de avaliação esta
                #preparado para receber.
                recommendations_df, ratings_df = create_user_dataframes(user, scores_list)
                #calculo as métricas para cada usuário
                novelty, accuracy = calculate_metrics(recommendations_df, ratings_df, cutoff)

                novelty_scores.append(novelty)
                accuracy_scores.append(accuracy)

            # Calcular média das métricas
            avg_novelty = sum(novelty_scores) / len(novelty_scores)
            avg_accuracy = sum(accuracy_scores) / len(accuracy_scores)
            #Salvo a média das métricas para cada solução
            res.append(avg_accuracy)
            res.append(avg_novelty)

        out["F"] = np.array(res)


class NSGA2PyMoo(MOO):
    def __init__(self, cutoff, num_items, num_users, pop_size, n_gen, seed=None):
        self.cutoff = cutoff
        self.num_items = num_items
        self.num_users = num_users
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.seed = seed

    def recommend(self, ratings=None, **kwargs):
        cutoff = self.cutoff
        num_items = self.num_items
        num_users = self.num_users
        pop_size = self.pop_size
        n_gen = self.n_gen
        seed = self.seed

        problem = FitnessEvaluation(13, 5, num_items, num_users, ratings, cutoff, 'x')
        algorithm = NSGA2(pop_size=pop_size)
        termination = ("n_gen", n_gen)
        res = minimize(problem, algorithm, termination, seed)#Trocar por maximizar?

        X = res.X
        F = res.F


        #Decisão, fazer função separada depois
        accuracy_index = 1  # A decisão é tomada dando preferência a acurácia - trocar por 2 depois
        # Sort solutions by accuracy in descending order
        sorted_X = X[F[:, accuracy_index].argsort()[::-1]]

        # Select the best solution (the first one after sorting)
        best_solution_X = sorted_X[0]
        df_best_solution_X = decode_recommendations(best_solution_X, num_items, num_users)
        print("----------------1")
        print(df_best_solution_X)
        print("----------------2")
        print(X)
        return df_best_solution_X

class NSGA3PyMoo(MOO):
    def __init__(self, cutoff, num_items, num_users, pop_size, n_gen, num_partitions, seed=None):
        self.cutoff = cutoff
        self.num_items = num_items
        self.num_users = num_users
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.num_partitions = num_partitions
        self.seed = seed

    def recommend(self, users, n, candidates=None, ratings=None, **kwargs):
        cutoff = self.cutoff
        num_items = self.num_items
        num_users = self.num_users
        pop_size = self.pop_size
        n_gen = self.n_gen
        num_partitions = self.num_partitions
        seed = self.seed
        num_objectives = 3

        ref_dirs = get_reference_directions("uniform", num_objectives, n_partitions=num_partitions)
        problem = FitnessEvaluation(num_items, num_users, ratings, cutoff)
        algorithm = NSGA3(pop_size=pop_size,ref_dirs=ref_dirs)
        termination = ("n_gen", n_gen)
        res = minimize(problem, algorithm, termination, seed)

        X = res.X
        F = res.F

        accuracy_index = 2 #A decisão é tomada dando preferência a acurácia
        # Sort solutions by accuracy in descending order
        sorted_X = X[F[:, accuracy_index].argsort()[::-1]]

        # Select the best solution (the first one after sorting)
        best_solution_X = sorted_X[0]
        df_best_solution_X = decode_recommendations(best_solution_X, num_items, num_users)
        print("----------------1")
        print(df_best_solution_X)
        print("----------------2")
        print(X)
        return df_best_solution_X


class AGEMOEAPyMoo(MOO):
    def __init__(self, cutoff, num_items, num_users, pop_size, n_gen, seed=None):
        self.cutoff = cutoff
        self.num_items = num_items
        self.num_users = num_users
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.seed = seed

    def recommend(self, users, n, candidates=None, ratings=None, **kwargs):
        cutoff = self.cutoff
        num_items = self.num_items
        num_users = self.num_users
        pop_size = self.pop_size
        n_gen = self.n_gen
        seed = self.seed

        problem = FitnessEvaluation(num_items, num_users, ratings, cutoff)
        algorithm = AGEMOEA(pop_size=pop_size)
        termination = ("n_gen", n_gen)
        res = minimize(problem, algorithm, termination, seed)

        X = res.X
        F = res.F
        accuracy_index = 2

        sorted_X = X[F[:, accuracy_index].argsort()[::-1]]


        best_solution_X = sorted_X[0]
        df_best_solution_X = decode_recommendations(best_solution_X, num_items, num_users)
        print("----------------1")
        print(df_best_solution_X)
        print("----------------2")
        print(X)
        return df_best_solution_X