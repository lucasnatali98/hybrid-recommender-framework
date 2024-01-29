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
from pymoo.operators.crossover.sbx import SBX


import json
import os


def experiments():
    #-----------------------------FWLS---------------------------------------FWLS---------------------------------------FWLS---------------------------------------FWLS---------------------------------------
    #FOLD 1--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #PROCESSANDO FILES
    file_keys = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold1/test.keys'
    file_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold1/FWLS-all-test.skl'
    output_file_merged_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold1/FWLS-all-test.merged'

    merge_files(file_keys, file_test, output_file_merged_test)

    # SALVANDO FEATURES DE TREINO E TESTE EM MEMÓRIA
    test_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold1/FWLS-all-test.merged')
    train_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold1/FWLS-all-train.merged')

    all_ratings = get_all_ratings(train_features_in_memory_dict)
    df_all_ratings = pd.DataFrame(all_ratings, columns=['user', 'item', 'rating'])
    preferences_dict, num_users_with_preference = generate_item_frequency_dict(ratings_df=df_all_ratings)

    top_n = 5
    epc = EPC(cutoff=top_n, preferences_dict=preferences_dict, num_users_with_preference=num_users_with_preference)
    ndcg = SklearnNDCG()

    '''
        Experimento 1
        Fold: 1
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: GaussianMutation
            Crossover: TwoPointCrossover
            top_n: 5
        '''

    experiment = 1
    pop_size = 100
    num_features = 657
    seed = 1
    mutation=GM()
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

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
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: PolynomialMutation
            Crossover: TwoPointCrossover
            top_n: 5
    '''

    '''
    experiment = 2
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 3
        Fold: 1
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: PolynomialMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''


    '''experiment = 3
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 4
        Fold: 1
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: GaussianMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 4
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = GM()
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 5
        Fold: 1
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: GaussianMutation
            Crossover: TwoPointCrossover
            top_n: 5
        '''

    '''
    experiment = 5
    pop_size = 500
    num_features = 657
    seed = 1
    mutation=GM()
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 6
        Fold: 1
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: PolynomialMutation
            Crossover: TwoPointCrossover
            top_n: 5
    '''

    '''
    experiment = 6
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 7
        Fold: 1
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: PolynomialMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 7
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 8
        Fold: 1
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: GaussianMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 8
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = GM()
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold1/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    # FOLD 2--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # PROCESSANDO FILES
    file_keys = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold2/test.keys'
    file_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold2/FWLS-all-test.skl'
    output_file_merged_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold2/FWLS-all-test.merged'

    merge_files(file_keys, file_test, output_file_merged_test)

    # SALVANDO FEATURES DE TREINO E TESTE EM MEMÓRIA
    test_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold2/FWLS-all-test.merged')
    train_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold2/FWLS-all-train.merged')

    all_ratings = get_all_ratings(train_features_in_memory_dict)
    df_all_ratings = pd.DataFrame(all_ratings, columns=['user', 'item', 'rating'])
    preferences_dict, num_users_with_preference = generate_item_frequency_dict(ratings_df=df_all_ratings)

    top_n = 5
    epc = EPC(cutoff=top_n, preferences_dict=preferences_dict, num_users_with_preference=num_users_with_preference)
    ndcg = SklearnNDCG()

    '''
        Experimento 9
        Fold: 2
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: GaussianMutation
            Crossover: TwoPointCrossover
            top_n: 5
        '''

    '''
    experiment = 9
    pop_size = 100
    num_features = 657
    seed = 1
    mutation=GM()
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 10
        Fold: 2
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: PolynomialMutation
            Crossover: TwoPointCrossover
            top_n: 5
    '''

    '''
    experiment = 10
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 11
        Fold: 2
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: PolynomialMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 11
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 12
        Fold: 2
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: GaussianMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 12
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = GM()
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 13
        Fold: 2
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: GaussianMutation
            Crossover: TwoPointCrossover
            top_n: 5
        '''

    '''
    experiment = 13
    pop_size = 500
    num_features = 657
    seed = 1
    mutation=GM()
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 14
        Fold: 2
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: PolynomialMutation
            Crossover: TwoPointCrossover
            top_n: 5
    '''

    '''
    experiment = 14
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 15
        Fold: 2
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: PolynomialMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 15
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 16
        Fold: 2
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: GaussianMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 16
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = GM()
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold2/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution_{mutation}.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    # FOLD 3--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # PROCESSANDO FILES
    file_keys = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold3/test.keys'
    file_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold3/FWLS-all-test.skl'
    output_file_merged_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold3/FWLS-all-test.merged'

    merge_files(file_keys, file_test, output_file_merged_test)

    # SALVANDO FEATURES DE TREINO E TESTE EM MEMÓRIA
    test_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold3/FWLS-all-test.merged')
    train_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold3/FWLS-all-train.merged')

    all_ratings = get_all_ratings(train_features_in_memory_dict)
    df_all_ratings = pd.DataFrame(all_ratings, columns=['user', 'item', 'rating'])
    preferences_dict, num_users_with_preference = generate_item_frequency_dict(ratings_df=df_all_ratings)

    top_n = 5
    epc = EPC(cutoff=top_n, preferences_dict=preferences_dict, num_users_with_preference=num_users_with_preference)
    ndcg = SklearnNDCG()

    '''
        Experimento 17
        Fold: 3
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: GaussianMutation
            Crossover: TwoPointCrossover
            top_n: 5
        '''

    '''
    experiment = 17
    pop_size = 100
    num_features = 657
    seed = 1
    mutation=GM()
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 18
        Fold: 3
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: PolynomialMutation
            Crossover: TwoPointCrossover
            top_n: 5
    '''

    '''
    experiment = 18
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 19
        Fold: 3
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: PolynomialMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 19
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 20
        Fold: 3
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: GaussianMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 20
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = GM()
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 21
        Fold: 3
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: GaussianMutation
            Crossover: TwoPointCrossover
            top_n: 5
        '''

    '''
    experiment = 21
    pop_size = 500
    num_features = 657
    seed = 1
    mutation=GM()
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 22
        Fold: 3
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: PolynomialMutation
            Crossover: TwoPointCrossover
            top_n: 5
    '''

    '''
    experiment = 22
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 23
        Fold: 3
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: PolynomialMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 23
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 24
        Fold: 3
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: GaussianMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 24
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = GM()
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold3/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    # FOLD 4--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # PROCESSANDO FILES
    file_keys = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold4/test.keys'
    file_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold4/FWLS-all-test.skl'
    output_file_merged_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold4/FWLS-all-test.merged'

    merge_files(file_keys, file_test, output_file_merged_test)

    # SALVANDO FEATURES DE TREINO E TESTE EM MEMÓRIA
    test_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold4/FWLS-all-test.merged')
    train_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold4/FWLS-all-train.merged')

    all_ratings = get_all_ratings(train_features_in_memory_dict)
    df_all_ratings = pd.DataFrame(all_ratings, columns=['user', 'item', 'rating'])
    preferences_dict, num_users_with_preference = generate_item_frequency_dict(ratings_df=df_all_ratings)

    top_n = 5
    epc = EPC(cutoff=top_n, preferences_dict=preferences_dict, num_users_with_preference=num_users_with_preference)
    ndcg = SklearnNDCG()

    '''
        Experimento 25
        Fold: 4
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: GaussianMutation
            Crossover: TwoPointCrossover
            top_n: 5
        '''

    '''
    experiment = 25
    pop_size = 100
    num_features = 657
    seed = 1
    mutation=GM()
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 26
        Fold: 4
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: PolynomialMutation
            Crossover: TwoPointCrossover
            top_n: 5
    '''

    '''
    experiment = 26
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 27
        Fold: 4
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: PolynomialMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 27
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 28
        Fold: 4
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: GaussianMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 28
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = GM()
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 29
        Fold: 4
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: GaussianMutation
            Crossover: TwoPointCrossover
            top_n: 5
        '''

    '''
    experiment = 29
    pop_size = 500
    num_features = 657
    seed = 1
    mutation=GM()
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 30
        Fold: 4
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: PolynomialMutation
            Crossover: TwoPointCrossover
            top_n: 5
    '''

    '''
    experiment = 30
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 31
        Fold: 4
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: PolynomialMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 31
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 32
        Fold: 4
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: GaussianMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 32
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = GM()
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold4/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    # FOLD 5--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # PROCESSANDO FILES
    file_keys = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold5/test.keys'
    file_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold5/FWLS-all-test.skl'
    output_file_merged_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold5/FWLS-all-test.merged'

    merge_files(file_keys, file_test, output_file_merged_test)

    # SALVANDO FEATURES DE TREINO E TESTE EM MEMÓRIA
    test_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold5/FWLS-all-test.merged')
    train_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/clara.loris/PycharmProjects/RecSysExp/data_storage/fwls/fold5/FWLS-all-train.merged')

    all_ratings = get_all_ratings(train_features_in_memory_dict)
    df_all_ratings = pd.DataFrame(all_ratings, columns=['user', 'item', 'rating'])
    preferences_dict, num_users_with_preference = generate_item_frequency_dict(ratings_df=df_all_ratings)

    top_n = 5
    epc = EPC(cutoff=top_n, preferences_dict=preferences_dict, num_users_with_preference=num_users_with_preference)
    ndcg = SklearnNDCG()

    '''
        Experimento 33
        Fold: 5
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: GaussianMutation
            Crossover: TwoPointCrossover
            top_n: 5
        '''

    '''
    experiment = 33
    pop_size = 100
    num_features = 657
    seed = 1
    mutation=GM()
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 34
        Fold: 5
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: PolynomialMutation
            Crossover: TwoPointCrossover
            top_n: 5
    '''

    '''
    experiment = 34
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 35
        Fold: 5
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: PolynomialMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 35
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 36
        Fold: 5
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: GaussianMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 36
    pop_size = 100
    num_features = 657
    seed = 1
    mutation = GM()
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop100'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 37
        Fold: 5
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: GaussianMutation
            Crossover: TwoPointCrossover
            top_n: 5
        '''

    '''
    experiment = 37
    pop_size = 500
    num_features = 657
    seed = 1
    mutation=GM()
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 38
        Fold: 5
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: PolynomialMutation
            Crossover: TwoPointCrossover
            top_n: 5
    '''

    '''
    experiment = 38
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 39
        Fold: 5
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: PolynomialMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 39
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = PM(eta=20)
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop500'
    file_name_best_solution = f'experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''

    '''
        Experimento 40
        Fold: 5
        Hibridização: FWLS
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: GaussianMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    '''
    experiment = 40
    pop_size = 500
    num_features = 657
    seed = 1
    mutation = GM()
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    #file_path_save_solution = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/fwls/fold5/pop500'
    file_name_best_solution = f'experiment_{experiment}_experiment_{experiment}_best_solution.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result.json'
    best_solution = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)

    # PREDICT PARA TODOS OS USUÁRIOS NSGA2
    file_name_test_predict = f'experiment_{experiment}_test_predict_all_users.json'
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
    file_name_result_test = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_result_test= os.path.join(folder_path, file_name_result_test)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_result_test, 'w') as file:
        json.dump(X.tolist(), file)
    print(average_novelty)
    print(average_accuracy)'''
if __name__ == "__main__":
    experiments()