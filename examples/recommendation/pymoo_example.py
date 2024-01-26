import numpy as np
import pandas as pd
from src.data.movielens import MovieLens
from src.recommenders.moo import NSGA2PyMoo
from src.recommenders.moo import NSGA3PyMoo
from src.recommenders.moo import AGEMOEAPyMoo
from src.recommenders.moo import decide_best_solution, get_all_ratings, create_user_dataframes
from src.utils import merge_files, read_and_store_features_in_memory
from src.metrics.epc import generate_item_frequency_dict
from src.metrics.epc import EPC
from src.metrics.ndcg import LenskitNDCG

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
    num_partitions = 12

    #SALVANDO FEATURES DE TREINO E TESTE EM MEMÓRIA
    test_features_in_memory_dict = read_and_store_features_in_memory(path_file_features='/home/usuario/PycharmProjects/RecSysExp/data_storage/hr/HR-all-test.merged')
    train_features_in_memory_dict = read_and_store_features_in_memory(path_file_features='/home/usuario/PycharmProjects/RecSysExp/data_storage/hr/HR-all-train.merged')

    all_ratings = get_all_ratings(train_features_in_memory_dict)
    df_all_ratings = pd.DataFrame(all_ratings, columns=['user', 'item', 'rating'])
    preferences_dict, num_users_with_preference = generate_item_frequency_dict(ratings_df=df_all_ratings)

    print(preferences_dict)

    parameters={
        "k": "None",
        "sample_weight": "None",
        "ignore_ties": "false"
    }

    epc = EPC(cutoff=top_n, preferences_dict=preferences_dict, num_users_with_preference=num_users_with_preference)
    ndcg = LenskitNDCG(parameters)

    metrics_to_use = [EPC, LenskitNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict, "num_users_with_preference": num_users_with_preference},
                     LenskitNDCG: {"parameters": parameters}}


    #NSGA2
    nsga2 = NSGA2PyMoo(pop_size, n_gen, top_n, num_features, seed)
    X,F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use, metric_params=metric_params)

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
    topn_scores = nsga2.predict(test_features_in_memory_dict, loaded_best_solution, top_n)

    novelty_scores = []
    accuracy_scores = []
    for user, scores_list in topn_scores.items():
        recommendations_user_df = create_user_dataframes(user, scores_list)
        epc_score = epc.evaluate(recommendations_user_df, df_all_ratings)
        ndcg_score = ndcg.evaluate(recommendations_user_df, df_all_ratings)
        print(df_all_ratings)
        print(recommendations_user_df)
        novelty_scores.append(epc_score)
        accuracy_scores.append(ndcg_score)

    # Calcular média das métricas
    avg_novelty = sum(novelty_scores) / len(novelty_scores)
    avg_accuracy = sum(accuracy_scores) / len(accuracy_scores)
    print("Resultado")
    print(avg_accuracy)
    print(avg_novelty)
    #PREDICT PARA UM USUÁRIO ESPECÍFICO NSGA2
    topn_user = nsga2.predict_for_user(1002, test_features_in_memory_dict, loaded_best_solution, top_n)
    recommendations_user_df = create_user_dataframes(1002, topn_user)
    epc_score = epc.evaluate(recommendations_user_df, df_all_ratings)
    ndcg_score = ndcg.evaluate(recommendations_user_df, df_all_ratings)
    print(epc_score)
    print(ndcg_score)

    '''nsga3 = NSGA3PyMoo(pop_size, n_gen, top_n, num_features, num_partitions,seed)
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

    '''agemoea = AGEMOEAPyMoo(pop_size, n_gen, top_n, num_features, seed)
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
    topn_user = agemoea.predict_for_user(1002, test_features_in_memory_dict, loaded_best_solution, top_n)'''

if __name__ == "__main__":
    example1()