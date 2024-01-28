import numpy as np
import pandas as pd
from src.recommenders.moo import NSGA2PyMoo
from src.recommenders.moo import NSGA3PyMoo
from src.recommenders.moo import AGEMOEAPyMoo
from src.recommenders.moo import decide_best_solution, get_all_ratings, create_user_dataframes
from src.utils import merge_files, read_and_store_features_in_memory
from src.metrics.epc import generate_item_frequency_dict
from src.metrics.epc import EPC
from src.metrics.ndcg import SklearnNDCG

from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.mutation.pm import PM
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.crossover.ux import UniformCrossover
from pymoo.operators.mutation.gauss import GM

import json
import os


def experiments():
    #-----------------------------FWLS---------------------------------------FWLS---------------------------------------FWLS---------------------------------------FWLS---------------------------------------
    #FOLD 1--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #PROCESSANDO FILES
    file_keys = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/stream/fold1/test.keys'
    file_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/stream/fold1/STREAM-all-test.skl'
    output_file_merged_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/stream/fold1/STREAM-all-test.merged'

    merge_files(file_keys, file_test, output_file_merged_test)

    # SALVANDO FEATURES DE TREINO E TESTE EM MEMÓRIA
    test_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/usuario/PycharmProjects/RecSysExp/data_storage/stream/fold1/STREAM-all-test.merged')
    train_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/usuario/PycharmProjects/RecSysExp/data_storage/stream/fold1/STREAM-all-train.merged')

    all_ratings = get_all_ratings(train_features_in_memory_dict)
    df_all_ratings = pd.DataFrame(all_ratings, columns=['user', 'item', 'rating'])
    preferences_dict, num_users_with_preference = generate_item_frequency_dict(ratings_df=df_all_ratings)

    top_n = 5
    epc = EPC(cutoff=top_n, preferences_dict=preferences_dict, num_users_with_preference=num_users_with_preference)
    ndcg = SklearnNDCG()

    '''
        Experimento 1
        Fold: 1
        Hibridização: STREAM
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: GaussianMutation
            Crossover: TwoPointCrossover
            top_n: 5
        '''

    pop_size = 100
    num_features = 56
    seed = 1
    mutation=GM()
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "00:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/stream/fold1/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/stream/fold1/pop100'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'test_predict_all_users_{mutation}_{crossover}.json'
    topn_scores = nsga2.predict(test_features_in_memory_dict, best_solution, top_n, folder_path, file_name_test_predict)

    novelty_scores = []
    accuracy_scores = []

    for user, scores_list in topn_scores.items():
        recommendations_user_df, ratings_user_df = create_user_dataframes(user, scores_list)

        epc_score = epc.evaluate(recommendations_user_df, df_all_ratings)
        ndcg_score = ndcg.evaluate(recommendations_user_df, ratings_user_df)

        novelty_scores.append(epc_score)
        accuracy_scores.append(ndcg_score)

    # Calcular médias ou métrica geral para todas as avaliações
    average_novelty = sum(novelty_scores) / len(novelty_scores)
    average_accuracy = sum(accuracy_scores) / len(accuracy_scores)
    file_name_result_test = f'test_result_{mutation}_{crossover}.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)

    '''
            Experimento 2
            Fold: 1
            Hibridização: STREAM
            Otimização:
                Meta heuristíca: NSGA2
                Pop: 100
                Mutation: PolynomialMutation
                Crossover: TwoPointCrossover
                top_n: 5
            '''

    '''pop_size = 100
    num_features = 56
    seed = 1
    mutation = PM(eta=20)
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "00:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/stream/fold1/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/stream/fold1/pop100'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'test_predict_all_users_{mutation}_{crossover}.json'
    topn_scores = nsga2.predict(test_features_in_memory_dict, best_solution, top_n, folder_path, file_name_test_predict)

    novelty_scores = []
    accuracy_scores = []

    for user, scores_list in topn_scores.items():
        recommendations_user_df, ratings_user_df = create_user_dataframes(user, scores_list)

        epc_score = epc.evaluate(recommendations_user_df, df_all_ratings)
        ndcg_score = ndcg.evaluate(recommendations_user_df, ratings_user_df)

        novelty_scores.append(epc_score)
        accuracy_scores.append(ndcg_score)

    # Calcular médias ou métrica geral para todas as avaliações
    average_novelty = sum(novelty_scores) / len(novelty_scores)
    average_accuracy = sum(accuracy_scores) / len(accuracy_scores)
    file_name_result_test = f'test_result_{mutation}_{crossover}.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''


if __name__ == "__main__":
    experiments()