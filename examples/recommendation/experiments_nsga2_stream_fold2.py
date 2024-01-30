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
from pymoo.visualization.scatter import Scatter
from pymoo.indicators.hv import Hypervolume

from scipy import stats



import json
import os


def experiments():

    # FOLD 2--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # PROCESSANDO FILES
    file_keys = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/stream/fold2/test.keys'
    file_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/stream/fold2/STREAM-all-test.skl'
    output_file_merged_test = '/home/clara.loris/PycharmProjects/RecSysExp/data_storage/stream/fold2/STREAM-all-test.merged'

    merge_files(file_keys, file_test, output_file_merged_test)

    # SALVANDO FEATURES DE TREINO E TESTE EM MEMÓRIA
    test_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/clara.loris/PycharmProjects/RecSysExp/data_storage/stream/fold2/STREAM-all-test.merged')
    train_features_in_memory_dict = read_and_store_features_in_memory(
        path_file_features='/home/clara.loris/PycharmProjects/RecSysExp/data_storage/stream/fold2/STREAM-all-train.merged')

    all_ratings = get_all_ratings(train_features_in_memory_dict)
    df_all_ratings = pd.DataFrame(all_ratings, columns=['user', 'item', 'rating'])
    preferences_dict, num_users_with_preference = generate_item_frequency_dict(ratings_df=df_all_ratings)

    top_n = 5
    epc = EPC(cutoff=top_n, preferences_dict=preferences_dict, num_users_with_preference=num_users_with_preference)
    ndcg = SklearnNDCG()

    '''
        Experimento 9
        Fold: 2
        Hibridização: STREAM
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: GaussianMutation
            Crossover: TwoPointCrossover
            top_n: 5
        '''

    experiment = 9
    pop_size = 100
    num_features = 59
    seed = 1
    mutation=GM()
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "00:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/stream/fold2/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    weights_decision1 = np.array([0.25, 0.75])
    weights_decision2 = np.array([0.75, 0.25])

    file_name_best_solution = f'experiment_{experiment}_best_solution_05_05.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result_05_05.json'
    file_name_best_solution1 = f'experiment_{experiment}_best_solution_25_75.json'
    file_name_best_solution_result1 = f'experiment_{experiment}_best_solution_result_25_75.json'
    file_name_best_solution2 = f'experiment_{experiment}_best_solution_75_25.json'
    file_name_best_solution_result2 = f'experiment_{experiment}_best_solution_result_75_25.json'

    best_solution, best_solution_index = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)
    best_solution1, best_solution_index1 = decide_best_solution(X, F, weights_decision1, folder_path, file_name_best_solution1, file_name_best_solution_result1)
    best_solution2, best_solution_index2 = decide_best_solution(X, F, weights_decision2, folder_path, file_name_best_solution2, file_name_best_solution_result2)

    plot = Scatter()
    plot.add(F, facecolor="none", edgecolor="red")
    plot.add(F[best_solution_index], facecolor="none", edgecolor="blue", s=200)
    plot.add(F[best_solution_index1], facecolor="none", edgecolor="orange", s=200)
    plot.add(F[best_solution_index2], facecolor="none", edgecolor="green", s=200)
    plot.save(os.path.join(folder_path, f'experiment_{experiment}_nsga2_pareto.png'))

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

    result_test = [average_novelty, average_accuracy]

    #Salvar resultados teste
    file_name_test_result = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_test_result = os.path.join(folder_path, file_name_test_result)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_test_result, 'w') as file:
        json.dump(result_test, file)


    #Intervalo de confiança
    # Calcular intervalo de confiança para a métrica de novidade
    novelty_conf_interval = stats.t.interval(0.95, len(novelty_scores) - 1, loc=average_novelty, scale=stats.sem(novelty_scores))

    # Calcular intervalo de confiança para a métrica de acurácia
    accuracy_conf_interval = stats.t.interval(0.95, len(accuracy_scores) - 1, loc=average_accuracy, scale=stats.sem(accuracy_scores))

    # Imprimir os intervalos de confiança
    print("Intervalo de Confiança para Novidade:", novelty_conf_interval)
    print("Intervalo de Confiança para Acurácia:", accuracy_conf_interval)

    #Hipervolume
    # Crie uma instância do Hypervolume
    approx_ideal = F.min(axis=0)
    approx_nadir = F.max(axis=0)
    hv_calculator = Hypervolume(ref_point=np.array([1.1, 1.1]), norm_ref_point=False, zero_to_one=True,
                                ideal=approx_ideal, nadir=approx_nadir)
    hv_value = hv_calculator.do(F)

    experiment_result = {
        "experiment": experiment,
        "average_novelty": average_novelty,
        "average_accuracy": average_accuracy,
        "hypervolume": hv_value,
        "novelty_conf_interval": novelty_conf_interval,
        "accuracy_conf_interval": accuracy_conf_interval,
    }

    # Salvar resultados experimento
    file_name_experiment = f'experiment_{experiment}.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_experiment= os.path.join(folder_path, file_name_experiment)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_experiment, 'w') as file:
        json.dump(experiment_result, file)

    print(average_novelty)
    print(average_accuracy)

    '''
        Experimento 10
        Fold: 2
        Hibridização: STREAM
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: PolynomialMutation
            Crossover: TwoPointCrossover
            top_n: 5
    '''

    experiment = 10
    pop_size = 100
    num_features = 59
    seed = 1
    mutation = PM(eta=20)
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "00:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/stream/fold2/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    weights_decision1 = np.array([0.25, 0.75])
    weights_decision2 = np.array([0.75, 0.25])

    file_name_best_solution = f'experiment_{experiment}_best_solution_05_05.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result_05_05.json'
    file_name_best_solution1 = f'experiment_{experiment}_best_solution_25_75.json'
    file_name_best_solution_result1 = f'experiment_{experiment}_best_solution_result_25_75.json'
    file_name_best_solution2 = f'experiment_{experiment}_best_solution_75_25.json'
    file_name_best_solution_result2 = f'experiment_{experiment}_best_solution_result_75_25.json'

    best_solution, best_solution_index = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)
    best_solution1, best_solution_index1 = decide_best_solution(X, F, weights_decision1, folder_path, file_name_best_solution1, file_name_best_solution_result1)
    best_solution2, best_solution_index2 = decide_best_solution(X, F, weights_decision2, folder_path, file_name_best_solution2, file_name_best_solution_result2)

    plot = Scatter()
    plot.add(F, facecolor="none", edgecolor="red")
    plot.add(F[best_solution_index], facecolor="none", edgecolor="blue", s=200)
    plot.add(F[best_solution_index1], facecolor="none", edgecolor="orange", s=200)
    plot.add(F[best_solution_index2], facecolor="none", edgecolor="green", s=200)
    plot.save(os.path.join(folder_path, f'experiment_{experiment}_nsga2_pareto.png'))

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

    result_test = [average_novelty, average_accuracy]

    #Salvar resultados teste
    file_name_test_result = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_test_result = os.path.join(folder_path, file_name_test_result)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_test_result, 'w') as file:
        json.dump(result_test, file)


    #Intervalo de confiança
    # Calcular intervalo de confiança para a métrica de novidade
    novelty_conf_interval = stats.t.interval(0.95, len(novelty_scores) - 1, loc=average_novelty, scale=stats.sem(novelty_scores))

    # Calcular intervalo de confiança para a métrica de acurácia
    accuracy_conf_interval = stats.t.interval(0.95, len(accuracy_scores) - 1, loc=average_accuracy, scale=stats.sem(accuracy_scores))

    # Imprimir os intervalos de confiança
    print("Intervalo de Confiança para Novidade:", novelty_conf_interval)
    print("Intervalo de Confiança para Acurácia:", accuracy_conf_interval)

    #Hipervolume
    # Crie uma instância do Hypervolume
    approx_ideal = F.min(axis=0)
    approx_nadir = F.max(axis=0)
    hv_calculator = Hypervolume(ref_point=np.array([1.1, 1.1]), norm_ref_point=False, zero_to_one=True,
                                ideal=approx_ideal, nadir=approx_nadir)
    hv_value = hv_calculator.do(F)

    experiment_result = {
        "experiment": experiment,
        "average_novelty": average_novelty,
        "average_accuracy": average_accuracy,
        "hypervolume": hv_value,
        "novelty_conf_interval": novelty_conf_interval,
        "accuracy_conf_interval": accuracy_conf_interval,
    }

    # Salvar resultados experimento
    file_name_experiment = f'experiment_{experiment}.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_experiment= os.path.join(folder_path, file_name_experiment)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_experiment, 'w') as file:
        json.dump(experiment_result, file)

    print(average_novelty)
    print(average_accuracy)

    '''
        Experimento 11
        Fold: 2
        Hibridização: STREAM
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: PolynomialMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    experiment = 11
    pop_size = 100
    num_features = 59
    seed = 1
    mutation = PM(eta=20)
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "00:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/stream/fold2/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    weights_decision1 = np.array([0.25, 0.75])
    weights_decision2 = np.array([0.75, 0.25])

    file_name_best_solution = f'experiment_{experiment}_best_solution_05_05.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result_05_05.json'
    file_name_best_solution1 = f'experiment_{experiment}_best_solution_25_75.json'
    file_name_best_solution_result1 = f'experiment_{experiment}_best_solution_result_25_75.json'
    file_name_best_solution2 = f'experiment_{experiment}_best_solution_75_25.json'
    file_name_best_solution_result2 = f'experiment_{experiment}_best_solution_result_75_25.json'

    best_solution, best_solution_index = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)
    best_solution1, best_solution_index1 = decide_best_solution(X, F, weights_decision1, folder_path, file_name_best_solution1, file_name_best_solution_result1)
    best_solution2, best_solution_index2 = decide_best_solution(X, F, weights_decision2, folder_path, file_name_best_solution2, file_name_best_solution_result2)

    plot = Scatter()
    plot.add(F, facecolor="none", edgecolor="red")
    plot.add(F[best_solution_index], facecolor="none", edgecolor="blue", s=200)
    plot.add(F[best_solution_index1], facecolor="none", edgecolor="orange", s=200)
    plot.add(F[best_solution_index2], facecolor="none", edgecolor="green", s=200)
    plot.save(os.path.join(folder_path, f'experiment_{experiment}_nsga2_pareto.png'))

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

    result_test = [average_novelty, average_accuracy]

    #Salvar resultados teste
    file_name_test_result = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_test_result = os.path.join(folder_path, file_name_test_result)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_test_result, 'w') as file:
        json.dump(result_test, file)


    #Intervalo de confiança
    # Calcular intervalo de confiança para a métrica de novidade
    novelty_conf_interval = stats.t.interval(0.95, len(novelty_scores) - 1, loc=average_novelty, scale=stats.sem(novelty_scores))

    # Calcular intervalo de confiança para a métrica de acurácia
    accuracy_conf_interval = stats.t.interval(0.95, len(accuracy_scores) - 1, loc=average_accuracy, scale=stats.sem(accuracy_scores))

    # Imprimir os intervalos de confiança
    print("Intervalo de Confiança para Novidade:", novelty_conf_interval)
    print("Intervalo de Confiança para Acurácia:", accuracy_conf_interval)

    #Hipervolume
    # Crie uma instância do Hypervolume
    approx_ideal = F.min(axis=0)
    approx_nadir = F.max(axis=0)
    hv_calculator = Hypervolume(ref_point=np.array([1.1, 1.1]), norm_ref_point=False, zero_to_one=True,
                                ideal=approx_ideal, nadir=approx_nadir)
    hv_value = hv_calculator.do(F)

    experiment_result = {
        "experiment": experiment,
        "average_novelty": average_novelty,
        "average_accuracy": average_accuracy,
        "hypervolume": hv_value,
        "novelty_conf_interval": novelty_conf_interval,
        "accuracy_conf_interval": accuracy_conf_interval,
    }

    # Salvar resultados experimento
    file_name_experiment = f'experiment_{experiment}.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_experiment= os.path.join(folder_path, file_name_experiment)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_experiment, 'w') as file:
        json.dump(experiment_result, file)

    print(average_novelty)
    print(average_accuracy)

    '''
        Experimento 12
        Fold: 2
        Hibridização: STREAM
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 100
            Mutation: GaussianMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    experiment = 12
    pop_size = 100
    num_features = 59
    seed = 1
    mutation = GM()
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "00:30:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/stream/fold2/pop100'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    weights_decision1 = np.array([0.25, 0.75])
    weights_decision2 = np.array([0.75, 0.25])

    file_name_best_solution = f'experiment_{experiment}_best_solution_05_05.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result_05_05.json'
    file_name_best_solution1 = f'experiment_{experiment}_best_solution_25_75.json'
    file_name_best_solution_result1 = f'experiment_{experiment}_best_solution_result_25_75.json'
    file_name_best_solution2 = f'experiment_{experiment}_best_solution_75_25.json'
    file_name_best_solution_result2 = f'experiment_{experiment}_best_solution_result_75_25.json'

    best_solution, best_solution_index = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)
    best_solution1, best_solution_index1 = decide_best_solution(X, F, weights_decision1, folder_path, file_name_best_solution1, file_name_best_solution_result1)
    best_solution2, best_solution_index2 = decide_best_solution(X, F, weights_decision2, folder_path, file_name_best_solution2, file_name_best_solution_result2)

    plot = Scatter()
    plot.add(F, facecolor="none", edgecolor="red")
    plot.add(F[best_solution_index], facecolor="none", edgecolor="blue", s=200)
    plot.add(F[best_solution_index1], facecolor="none", edgecolor="orange", s=200)
    plot.add(F[best_solution_index2], facecolor="none", edgecolor="green", s=200)
    plot.save(os.path.join(folder_path, f'experiment_{experiment}_nsga2_pareto.png'))

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

    result_test = [average_novelty, average_accuracy]

    #Salvar resultados teste
    file_name_test_result = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_test_result = os.path.join(folder_path, file_name_test_result)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_test_result, 'w') as file:
        json.dump(result_test, file)


    #Intervalo de confiança
    # Calcular intervalo de confiança para a métrica de novidade
    novelty_conf_interval = stats.t.interval(0.95, len(novelty_scores) - 1, loc=average_novelty, scale=stats.sem(novelty_scores))

    # Calcular intervalo de confiança para a métrica de acurácia
    accuracy_conf_interval = stats.t.interval(0.95, len(accuracy_scores) - 1, loc=average_accuracy, scale=stats.sem(accuracy_scores))

    # Imprimir os intervalos de confiança
    print("Intervalo de Confiança para Novidade:", novelty_conf_interval)
    print("Intervalo de Confiança para Acurácia:", accuracy_conf_interval)

    #Hipervolume
    # Crie uma instância do Hypervolume
    approx_ideal = F.min(axis=0)
    approx_nadir = F.max(axis=0)
    hv_calculator = Hypervolume(ref_point=np.array([1.1, 1.1]), norm_ref_point=False, zero_to_one=True,
                                ideal=approx_ideal, nadir=approx_nadir)
    hv_value = hv_calculator.do(F)

    experiment_result = {
        "experiment": experiment,
        "average_novelty": average_novelty,
        "average_accuracy": average_accuracy,
        "hypervolume": hv_value,
        "novelty_conf_interval": novelty_conf_interval,
        "accuracy_conf_interval": accuracy_conf_interval,
    }

    # Salvar resultados experimento
    file_name_experiment = f'experiment_{experiment}.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_experiment= os.path.join(folder_path, file_name_experiment)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_experiment, 'w') as file:
        json.dump(experiment_result, file)

    print(average_novelty)
    print(average_accuracy)

    '''
        Experimento 13
        Fold: 2
        Hibridização: STREAM
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: GaussianMutation
            Crossover: TwoPointCrossover
            top_n: 5
        '''

    experiment = 13
    pop_size = 500
    num_features = 59
    seed = 1
    mutation=GM()
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:00:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/stream/fold2/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

   # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    weights_decision1 = np.array([0.25, 0.75])
    weights_decision2 = np.array([0.75, 0.25])

    file_name_best_solution = f'experiment_{experiment}_best_solution_05_05.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result_05_05.json'
    file_name_best_solution1 = f'experiment_{experiment}_best_solution_25_75.json'
    file_name_best_solution_result1 = f'experiment_{experiment}_best_solution_result_25_75.json'
    file_name_best_solution2 = f'experiment_{experiment}_best_solution_75_25.json'
    file_name_best_solution_result2 = f'experiment_{experiment}_best_solution_result_75_25.json'

    best_solution, best_solution_index = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)
    best_solution1, best_solution_index1 = decide_best_solution(X, F, weights_decision1, folder_path, file_name_best_solution1, file_name_best_solution_result1)
    best_solution2, best_solution_index2 = decide_best_solution(X, F, weights_decision2, folder_path, file_name_best_solution2, file_name_best_solution_result2)

    plot = Scatter()
    plot.add(F, facecolor="none", edgecolor="red")
    plot.add(F[best_solution_index], facecolor="none", edgecolor="blue", s=200)
    plot.add(F[best_solution_index1], facecolor="none", edgecolor="orange", s=200)
    plot.add(F[best_solution_index2], facecolor="none", edgecolor="green", s=200)
    plot.save(os.path.join(folder_path, f'experiment_{experiment}_nsga2_pareto.png'))

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

    result_test = [average_novelty, average_accuracy]

    #Salvar resultados teste
    file_name_test_result = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_test_result = os.path.join(folder_path, file_name_test_result)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_test_result, 'w') as file:
        json.dump(result_test, file)


    #Intervalo de confiança
    # Calcular intervalo de confiança para a métrica de novidade
    novelty_conf_interval = stats.t.interval(0.95, len(novelty_scores) - 1, loc=average_novelty, scale=stats.sem(novelty_scores))

    # Calcular intervalo de confiança para a métrica de acurácia
    accuracy_conf_interval = stats.t.interval(0.95, len(accuracy_scores) - 1, loc=average_accuracy, scale=stats.sem(accuracy_scores))

    # Imprimir os intervalos de confiança
    print("Intervalo de Confiança para Novidade:", novelty_conf_interval)
    print("Intervalo de Confiança para Acurácia:", accuracy_conf_interval)

    #Hipervolume
    # Crie uma instância do Hypervolume
    approx_ideal = F.min(axis=0)
    approx_nadir = F.max(axis=0)
    hv_calculator = Hypervolume(ref_point=np.array([1.1, 1.1]), norm_ref_point=False, zero_to_one=True,
                                ideal=approx_ideal, nadir=approx_nadir)
    hv_value = hv_calculator.do(F)

    experiment_result = {
        "experiment": experiment,
        "average_novelty": average_novelty,
        "average_accuracy": average_accuracy,
        "hypervolume": hv_value,
        "novelty_conf_interval": novelty_conf_interval,
        "accuracy_conf_interval": accuracy_conf_interval,
    }

    # Salvar resultados experimento
    file_name_experiment = f'experiment_{experiment}.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_experiment= os.path.join(folder_path, file_name_experiment)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_experiment, 'w') as file:
        json.dump(experiment_result, file)

    print(average_novelty)
    print(average_accuracy)

    '''
        Experimento 14
        Fold: 2
        Hibridização: STREAM
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: PolynomialMutation
            Crossover: TwoPointCrossover
            top_n: 5
    '''

    experiment = 14
    pop_size = 500
    num_features = 59
    seed = 1
    mutation = PM(eta=20)
    crossover = TwoPointCrossover(prob=0.9)
    time_termination = "01:00:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/stream/fold2/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    weights_decision1 = np.array([0.25, 0.75])
    weights_decision2 = np.array([0.75, 0.25])

    file_name_best_solution = f'experiment_{experiment}_best_solution_05_05.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result_05_05.json'
    file_name_best_solution1 = f'experiment_{experiment}_best_solution_25_75.json'
    file_name_best_solution_result1 = f'experiment_{experiment}_best_solution_result_25_75.json'
    file_name_best_solution2 = f'experiment_{experiment}_best_solution_75_25.json'
    file_name_best_solution_result2 = f'experiment_{experiment}_best_solution_result_75_25.json'

    best_solution, best_solution_index = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)
    best_solution1, best_solution_index1 = decide_best_solution(X, F, weights_decision1, folder_path, file_name_best_solution1, file_name_best_solution_result1)
    best_solution2, best_solution_index2 = decide_best_solution(X, F, weights_decision2, folder_path, file_name_best_solution2, file_name_best_solution_result2)

    plot = Scatter()
    plot.add(F, facecolor="none", edgecolor="red")
    plot.add(F[best_solution_index], facecolor="none", edgecolor="blue", s=200)
    plot.add(F[best_solution_index1], facecolor="none", edgecolor="orange", s=200)
    plot.add(F[best_solution_index2], facecolor="none", edgecolor="green", s=200)
    plot.save(os.path.join(folder_path, f'experiment_{experiment}_nsga2_pareto.png'))

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

    result_test = [average_novelty, average_accuracy]

    #Salvar resultados teste
    file_name_test_result = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_test_result = os.path.join(folder_path, file_name_test_result)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_test_result, 'w') as file:
        json.dump(result_test, file)


    #Intervalo de confiança
    # Calcular intervalo de confiança para a métrica de novidade
    novelty_conf_interval = stats.t.interval(0.95, len(novelty_scores) - 1, loc=average_novelty, scale=stats.sem(novelty_scores))

    # Calcular intervalo de confiança para a métrica de acurácia
    accuracy_conf_interval = stats.t.interval(0.95, len(accuracy_scores) - 1, loc=average_accuracy, scale=stats.sem(accuracy_scores))

    # Imprimir os intervalos de confiança
    print("Intervalo de Confiança para Novidade:", novelty_conf_interval)
    print("Intervalo de Confiança para Acurácia:", accuracy_conf_interval)

    #Hipervolume
    # Crie uma instância do Hypervolume
    approx_ideal = F.min(axis=0)
    approx_nadir = F.max(axis=0)
    hv_calculator = Hypervolume(ref_point=np.array([1.1, 1.1]), norm_ref_point=False, zero_to_one=True,
                                ideal=approx_ideal, nadir=approx_nadir)
    hv_value = hv_calculator.do(F)

    experiment_result = {
        "experiment": experiment,
        "average_novelty": average_novelty,
        "average_accuracy": average_accuracy,
        "hypervolume": hv_value,
        "novelty_conf_interval": novelty_conf_interval,
        "accuracy_conf_interval": accuracy_conf_interval,
    }

    # Salvar resultados experimento
    file_name_experiment = f'experiment_{experiment}.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_experiment= os.path.join(folder_path, file_name_experiment)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_experiment, 'w') as file:
        json.dump(experiment_result, file)

    print(average_novelty)
    print(average_accuracy)

    '''
        Experimento 15
        Fold: 2
        Hibridização: STREAM
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: PolynomialMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    experiment = 15
    pop_size = 500
    num_features = 59
    seed = 1
    mutation = PM(eta=20)
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:00:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/stream/fold2/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    weights_decision1 = np.array([0.25, 0.75])
    weights_decision2 = np.array([0.75, 0.25])

    file_name_best_solution = f'experiment_{experiment}_best_solution_05_05.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result_05_05.json'
    file_name_best_solution1 = f'experiment_{experiment}_best_solution_25_75.json'
    file_name_best_solution_result1 = f'experiment_{experiment}_best_solution_result_25_75.json'
    file_name_best_solution2 = f'experiment_{experiment}_best_solution_75_25.json'
    file_name_best_solution_result2 = f'experiment_{experiment}_best_solution_result_75_25.json'

    best_solution, best_solution_index = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)
    best_solution1, best_solution_index1 = decide_best_solution(X, F, weights_decision1, folder_path, file_name_best_solution1, file_name_best_solution_result1)
    best_solution2, best_solution_index2 = decide_best_solution(X, F, weights_decision2, folder_path, file_name_best_solution2, file_name_best_solution_result2)

    plot = Scatter()
    plot.add(F, facecolor="none", edgecolor="red")
    plot.add(F[best_solution_index], facecolor="none", edgecolor="blue", s=200)
    plot.add(F[best_solution_index1], facecolor="none", edgecolor="orange", s=200)
    plot.add(F[best_solution_index2], facecolor="none", edgecolor="green", s=200)
    plot.save(os.path.join(folder_path, f'experiment_{experiment}_nsga2_pareto.png'))

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

    result_test = [average_novelty, average_accuracy]

    #Salvar resultados teste
    file_name_test_result = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_test_result = os.path.join(folder_path, file_name_test_result)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_test_result, 'w') as file:
        json.dump(result_test, file)


    #Intervalo de confiança
    # Calcular intervalo de confiança para a métrica de novidade
    novelty_conf_interval = stats.t.interval(0.95, len(novelty_scores) - 1, loc=average_novelty, scale=stats.sem(novelty_scores))

    # Calcular intervalo de confiança para a métrica de acurácia
    accuracy_conf_interval = stats.t.interval(0.95, len(accuracy_scores) - 1, loc=average_accuracy, scale=stats.sem(accuracy_scores))

    # Imprimir os intervalos de confiança
    print("Intervalo de Confiança para Novidade:", novelty_conf_interval)
    print("Intervalo de Confiança para Acurácia:", accuracy_conf_interval)

    #Hipervolume
    # Crie uma instância do Hypervolume
    approx_ideal = F.min(axis=0)
    approx_nadir = F.max(axis=0)
    hv_calculator = Hypervolume(ref_point=np.array([1.1, 1.1]), norm_ref_point=False, zero_to_one=True,
                                ideal=approx_ideal, nadir=approx_nadir)
    hv_value = hv_calculator.do(F)

    experiment_result = {
        "experiment": experiment,
        "average_novelty": average_novelty,
        "average_accuracy": average_accuracy,
        "hypervolume": hv_value,
        "novelty_conf_interval": novelty_conf_interval,
        "accuracy_conf_interval": accuracy_conf_interval,
    }

    # Salvar resultados experimento
    file_name_experiment = f'experiment_{experiment}.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_experiment= os.path.join(folder_path, file_name_experiment)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_experiment, 'w') as file:
        json.dump(experiment_result, file)

    print(average_novelty)
    print(average_accuracy)

    '''
        Experimento 16
        Fold: 2
        Hibridização: STREAM
        Otimização:
            Meta heuristíca: NSGA2
            Pop: 500
            Mutation: GaussianMutation
            Crossover: SimulatedBinaryCrossover
            top_n: 5
    '''

    experiment = 16
    pop_size = 500
    num_features = 59
    seed = 1
    mutation = GM()
    crossover=SBX(eta=15, prob=0.9)
    time_termination = "01:00:00"
    metrics_to_use = [EPC, SklearnNDCG]
    metric_params = {EPC: {"cutoff": top_n, "preferences_dict": preferences_dict,
                           "num_users_with_preference": num_users_with_preference},
                     SklearnNDCG: {}}

    # NSGA2
    nsga2 = NSGA2PyMoo(pop_size, top_n, num_features, time_termination, mutation, crossover, seed, experiment)
    folder_path = 'PycharmProjects/RecSysExp/experiment_output/moo/nsga2/stream/fold2/pop500'
    X, F = nsga2.recommend(features_in_memory_dict=train_features_in_memory_dict, metrics=metrics_to_use,
                           metric_params=metric_params, folder_path=folder_path)

    # DECISÃO MELHOR SOLUÇÃO
    weights_decision = np.array([0.5, 0.5])
    weights_decision1 = np.array([0.25, 0.75])
    weights_decision2 = np.array([0.75, 0.25])

    file_name_best_solution = f'experiment_{experiment}_best_solution_05_05.json'
    file_name_best_solution_result = f'experiment_{experiment}_best_solution_result_05_05.json'
    file_name_best_solution1 = f'experiment_{experiment}_best_solution_25_75.json'
    file_name_best_solution_result1 = f'experiment_{experiment}_best_solution_result_25_75.json'
    file_name_best_solution2 = f'experiment_{experiment}_best_solution_75_25.json'
    file_name_best_solution_result2 = f'experiment_{experiment}_best_solution_result_75_25.json'

    best_solution, best_solution_index = decide_best_solution(X, F, weights_decision, folder_path, file_name_best_solution, file_name_best_solution_result)
    best_solution1, best_solution_index1 = decide_best_solution(X, F, weights_decision1, folder_path, file_name_best_solution1, file_name_best_solution_result1)
    best_solution2, best_solution_index2 = decide_best_solution(X, F, weights_decision2, folder_path, file_name_best_solution2, file_name_best_solution_result2)

    plot = Scatter()
    plot.add(F, facecolor="none", edgecolor="red")
    plot.add(F[best_solution_index], facecolor="none", edgecolor="blue", s=200)
    plot.add(F[best_solution_index1], facecolor="none", edgecolor="orange", s=200)
    plot.add(F[best_solution_index2], facecolor="none", edgecolor="green", s=200)
    plot.save(os.path.join(folder_path, f'experiment_{experiment}_nsga2_pareto.png'))

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

    result_test = [average_novelty, average_accuracy]

    #Salvar resultados teste
    file_name_test_result = f'experiment_{experiment}_test_result.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_test_result = os.path.join(folder_path, file_name_test_result)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_test_result, 'w') as file:
        json.dump(result_test, file)


    #Intervalo de confiança
    # Calcular intervalo de confiança para a métrica de novidade
    novelty_conf_interval = stats.t.interval(0.95, len(novelty_scores) - 1, loc=average_novelty, scale=stats.sem(novelty_scores))

    # Calcular intervalo de confiança para a métrica de acurácia
    accuracy_conf_interval = stats.t.interval(0.95, len(accuracy_scores) - 1, loc=average_accuracy, scale=stats.sem(accuracy_scores))

    # Imprimir os intervalos de confiança
    print("Intervalo de Confiança para Novidade:", novelty_conf_interval)
    print("Intervalo de Confiança para Acurácia:", accuracy_conf_interval)

    #Hipervolume
    # Crie uma instância do Hypervolume
    approx_ideal = F.min(axis=0)
    approx_nadir = F.max(axis=0)
    hv_calculator = Hypervolume(ref_point=np.array([1.1, 1.1]), norm_ref_point=False, zero_to_one=True,
                                ideal=approx_ideal, nadir=approx_nadir)
    hv_value = hv_calculator.do(F)

    experiment_result = {
        "experiment": experiment,
        "average_novelty": average_novelty,
        "average_accuracy": average_accuracy,
        "hypervolume": hv_value,
        "novelty_conf_interval": novelty_conf_interval,
        "accuracy_conf_interval": accuracy_conf_interval,
    }

    # Salvar resultados experimento
    file_name_experiment = f'experiment_{experiment}.json'

    folder_path = os.path.expanduser(f'~/{folder_path}')
    file_path_experiment= os.path.join(folder_path, file_name_experiment)
    os.makedirs(folder_path, exist_ok=True)

    with open(file_path_experiment, 'w') as file:
        json.dump(experiment_result, file)

    print(average_novelty)
    print(average_accuracy)

if __name__ == "__main__":
    experiments()