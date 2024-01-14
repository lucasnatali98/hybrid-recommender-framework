from src.recommenders.recommender import AbstractMultiObjectiveRecommender
import pandas as pd
import numpy as np

from src.metrics.epc import EPC
from src.metrics.diversity import RecmetricsDIVERSITY
from src.metrics.ndcg import LenskitNDCG
from src.metrics.recall import LenskitRecall

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

def decode_recommendations(design, num_items, num_users):
    # Binarize the matrix with a probability threshold of 0.9
    binary_x = (design > 0.9).astype(int)

    # Initialize an empty DataFrame to store recommendations
    recommendations_df = pd.DataFrame(columns=['user', 'item', 'score', 'algorithm_name'])

    # Parameters
    num_items = num_items
    num_users = num_users

    # Decode the recommendations
    for i, user_row in enumerate(binary_x.reshape((num_users, -1))):
        user_id = i + 1  # User IDs are 1-indexed

        # Find indices where user_row is 1
        recommended_items = np.where(user_row == 1)[0]

        # print(recommended_items)

        # Add recommendations to DataFrame
        user_recommendations = pd.DataFrame({
            'user': [user_id] * len(recommended_items),
            'item': i * num_items + recommended_items + 1,  # Item IDs are 1-indexed
            'score': design[i * num_items + recommended_items],
            'algorithm_name': 'nsga2'
        })

        recommendations_df = pd.concat([recommendations_df, user_recommendations])

    # Reset indices
    recommendations_df.reset_index(drop=True, inplace=True)

    return recommendations_df

class RecommenderProblem(Problem):
    def __init__(self, num_items, num_users, ratings, cutoff, df_features):
        super().__init__(n_var=num_users * num_items, n_obj=2, n_constr=0, xl=0, xu=1)

        self.num_items = num_items
        self.num_users = num_users
        self.ratings = ratings
        self.df_features = df_features
        self.cutoff = cutoff

    def _evaluate(self, designs, out, *args, **kwargs):
        ratings = self.ratings
        df_features = self.df_features

        parameters = {
            "labels": "None",
            "average": "binary",
            "sample_weight": "None",
            "zero_division": "warn"
        }

        cutoff = self.cutoff
        num_items = self.num_items
        num_users = self.num_users

        epc = EPC(cutoff)
        ild = RecmetricsDIVERSITY()
        # ndcg = LenskitNDCG(parameters)
        recall = LenskitRecall(parameters)

        res = []

        for design in designs:
            print('-------------------design-------------------')
            print(design)

            recommendations = decode_recommendations(design, num_items, num_users)
            print("------------decode---------------")
            print(recommendations)
            # x representa as recomendações para cada item (0 ou 1)recommendations_for_all_users
            # Avaliar métricas de novidade, diversidade e acurácia

            novelty = epc.evaluate(recommendations, ratings)
            #diversity = ild.evaluate(recommendations, df_features)  # Substitua isso pela sua função de diversidade
            accuracy = recall.evaluate(recommendations, ratings)

            res.append(novelty)
            res.append(accuracy)
            #res.append(diversity)
            print("------------teste")
            print(novelty)
            print(accuracy)
            #print(diversity)

        out["F"] = np.array(res)


class NSGA2PyMoo(MOO):
    def __init__(self, cutoff, num_items, num_users, pop_size, n_gen, seed=None):
        self.cutoff = cutoff
        self.num_items = num_items
        self.num_users = num_users
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.seed = seed

    def recommend(self, users, n, df_features, candidates=None, ratings=None, **kwargs):
        cutoff = self.cutoff
        num_items = self.num_items
        num_users = self.num_users
        pop_size = self.pop_size
        n_gen = self.n_gen
        seed = self.seed

        problem = RecommenderProblem(num_items, num_users, ratings, cutoff, df_features)
        algorithm = NSGA2(pop_size=pop_size)
        termination = ("n_gen", n_gen)
        res = minimize(problem, algorithm, termination, seed)

        X = res.X
        F = res.F
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
        num_objectives = 2

        ref_dirs = get_reference_directions("uniform", num_objectives, n_partitions=num_partitions)
        problem = RecommenderProblem(num_items, num_users, ratings, cutoff)
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

        problem = RecommenderProblem(num_items, num_users, ratings, cutoff)
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