import numpy as np
import pandas as pd
from src.data.movielens import MovieLens
from src.recommenders.moo import NSGA2PyMoo
from src.recommenders.moo import NSGA3PyMoo
from src.recommenders.moo import AGEMOEAPyMoo
from src.recommenders.moo import decide_best_solution
from src.utils import merge_files, read_and_store_features_in_memory
import json
import os


def example1():
    #PROCESSANDO FILES
    file_keys = '/home/usuario/PycharmProjects/RecSysExp/data_storage/hr/test.keys'
    file_test = '/home/usuario/PycharmProjects/RecSysExp/data_storage/hr/HR-all-test.skl'
    output_file_merged_test = '/home/usuario/PycharmProjects/RecSysExp/data_storage/hr/HR-all-test.merged'

    merge_files(file_keys, file_test, output_file_merged_test)

    relative_path_nsga2 = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2'
    relative_path_nsga3 = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga3'
    relative_path_agemoea = 'PycharmProjects/RecSysExp/experiment_output/moo/agemoea'

    file_name_X = 'pareto_front.json'
    file_name_F = 'results_solutions.json'
    file_name_best_solution = 'best_solution.json'

    folder_path_nsga2 = os.path.expanduser(f'~/{relative_path_nsga2}')
    folder_path_nsga3 = os.path.expanduser(f'~/{relative_path_nsga3}')
    folder_path_agemoea = os.path.expanduser(f'~/{relative_path_agemoea}')

    file_path_X_nsga2 = os.path.join(folder_path_nsga2, file_name_X)
    file_path_F_nsga2 = os.path.join(folder_path_nsga2, file_name_F)
    file_path_best_solution_nsga2 = os.path.join(folder_path_nsga2, file_name_best_solution)

    file_path_X_nsga3 = os.path.join(folder_path_nsga3, file_name_X)
    file_path_F_nsga3 = os.path.join(folder_path_nsga3, file_name_F)
    file_path_best_solution_nsga3 = os.path.join(folder_path_nsga3, file_name_best_solution)

    file_path_X_agemoea = os.path.join(folder_path_agemoea, file_name_X)
    file_path_F_agemoea = os.path.join(folder_path_agemoea, file_name_F)
    file_path_best_solution_agemoea = os.path.join(folder_path_agemoea, file_name_best_solution)

    top_n = 5
    pop_size = 5
    n_gen = 1
    num_features = 13
    seed = 1

    #SALVANDO FEATURES DE TREINO E TESTE EM MEMÓRIA
    test_features_in_memory_dict = read_and_store_features_in_memory(path_file_features='/home/usuario/PycharmProjects/RecSysExp/data_storage/hr/HR-all-test.merged')
    train_features_in_memory_dict = read_and_store_features_in_memory(path_file_features='/home/usuario/PycharmProjects/RecSysExp/data_storage/hr/HR-all-train.merged')

    #TREINO NSGA2
    '''nsga2 = NSGA2PyMoo(pop_size, n_gen, top_n, num_features, seed)
    X,F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict)

    with open(file_path_X_nsga2, 'r') as file:
        loaded_pareto_front = json.load(file)

    with open(file_path_F_nsga2, 'r') as file:
        loaded_results_pareto_front = json.load(file)

    #DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5,0.5])
    algorithm = 'nsga2'
    best_solution = decide_best_solution(loaded_pareto_front,loaded_results_pareto_front,weights_decision, algorithm)

    with open(file_path_best_solution_nsga2, 'r') as file:
        loaded_best_solution = json.load(file)

    #PREDICT PARA TODOS OS USUÁRIOS NSGA2
    topn_score = nsga2.predict(test_features_in_memory_dict, loaded_best_solution, top_n)
    #PREDICT PARA UM USUÁRIO ESPECÍFICO NSGA2
    topn_user = nsga2.predict_for_user(1002, test_features_in_memory_dict, loaded_best_solution, top_n)'''


    '''nsga3 = NSGA3PyMoo(pop_size=5, n_gen=2, top_n=5, num_features=13, num_partitions=12,seed=2)
    X,F = nsga3.recommend(features_in_memory_dict=train_features_in_memory_dict)

    with open(file_path_X_nsga3, 'r') as file:
        loaded_pareto_front = json.load(file)

    with open(file_path_F_nsga3, 'r') as file:
        loaded_results_pareto_front = json.load(file)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    algorithm = 'nsga3'
    best_solution = decide_best_solution(loaded_pareto_front, loaded_results_pareto_front, weights_decision, algorithm)

    with open(file_path_best_solution_nsga3, 'r') as file:
        loaded_best_solution = json.load(file)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA3
    topn_score = nsga3.predict(test_features_in_memory_dict, loaded_best_solution, top_n)
    # PREDICT PARA UM USUÁRIO ESPECÍFICO NSGA3
    topn_user = nsga3.predict_for_user(1002, test_features_in_memory_dict, loaded_best_solution, top_n)'''

    agemoea = AGEMOEAPyMoo(pop_size=5, n_gen=2, top_n=5, num_features=13, seed=2)
    X,F = agemoea.recommend(features_in_memory_dict=train_features_in_memory_dict)

    with open(file_path_X_agemoea, 'r') as file:
        loaded_pareto_front = json.load(file)

    with open(file_path_F_agemoea, 'r') as file:
        loaded_results_pareto_front = json.load(file)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    algorithm = 'agemoea'
    best_solution = decide_best_solution(loaded_pareto_front, loaded_results_pareto_front, weights_decision, algorithm)

    with open(file_path_best_solution_agemoea, 'r') as file:
        loaded_best_solution = json.load(file)

    # PREDICT PARA TODOS OS USUÁRIOS AGEMOEA
    topn_score = agemoea.predict(test_features_in_memory_dict, loaded_best_solution, top_n)
    # PREDICT PARA UM USUÁRIO ESPECÍFICO AGEMOEA
    topn_user = agemoea.predict_for_user(1002, test_features_in_memory_dict, loaded_best_solution, top_n)

if __name__ == "__main__":
    example1()