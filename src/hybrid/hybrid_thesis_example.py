from src.hybrid.hybrid import HybridWeighted
from src.utils import process_parameters
from pandas import DataFrame, Series, read_csv, merge
from src.utils import hrf_experiment_output_path, hrf_metafeatures_path
from src.metafeatures.metafeature import read_metafeatures_textfiles
from src.data.movielens import MovieLens
from src.data.loader import Loader
from sklearn.datasets import load_svmlight_file, dump_svmlight_file
import numpy as np
import re
from sklearn.linear_model import LinearRegression
import sys
import time
from datetime import datetime
from scipy.stats import uniform as uniform
from scipy.stats import randint as randint
from sklearn.linear_model import Ridge
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import SGDRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import LinearSVR
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV

rec_temp_files_path = hrf_experiment_output_path().joinpath("rec_temp_files")
svmlight_files_path = hrf_experiment_output_path().joinpath("svmlight_files")

algorithms = {
    'Ridge': (Ridge(), {'alpha': [0.1,0.2,0.3,1,2,3,4,5], 'fit_intercept': [True, False]}, 'R'),
    'B-Ridge': (BayesianRidge(),
                {'n_iter': np.random.uniform(100, 600, 10), 'alpha_1': np.random.uniform(0.000001, 1, 10), 'alpha_2': np.random.uniform(0.000001, 1, 10),
                 'lambda_1': np.random.uniform(0.000001, 1, 10), 'lambda_2': np.random.uniform(0.000001, 1, 10)}, 'R'),
    # 'Bag'      : ( BaggingRegressor(n_jobs=-1, random_state=0), {'n_estimators': randint(10, 500), 'max_samples': randint(1, 50), 'max_features': randint(1, 50), 'bootstrap': [True, False], 'bootstrap_features': [True, False], 'oob_score': [True, False]}, 'R' ),
    'Bag': (BaggingRegressor(n_jobs=1, random_state=0, bootstrap=True),
            {'n_estimators': randint(10, 500), 'max_samples': randint(1, 50), 'bootstrap_features': [True, False],
             'oob_score': [True, False]}, 'R'),
    # 'RFR'      : ( RandomForestRegressor(n_jobs=-1, random_state=0), {'n_estimators': randint(10, 500), 'max_features': [None, randint(1, 50)], 'max_depth': [None, randint(1, 50)], 'min_samples_split': randint(2, 50), 'min_samples_leaf': randint(1, 50), 'min_weight_fraction_leaf': uniform(0.0, 1.0), 'max_leaf_nodes': [None, randint(1, 50)], 'bootstrap': [True, False], 'oob_score': [True, False]}, 'R' ),
    'RFR': (RandomForestRegressor(n_jobs=-1, random_state=0, bootstrap=True),
            {'n_estimators': randint(10, 500), 'max_depth': randint(1, 50), 'min_samples_split': randint(2, 50),
             'min_samples_leaf': randint(1, 50), 'min_weight_fraction_leaf': uniform(0.0, 0.5),
             'max_leaf_nodes': randint(2, 50)}, 'R'),
    'AdaB': (AdaBoostRegressor(random_state=0), {'n_estimators': randint(10, 500), 'learning_rate': uniform(0.05, 2.0),
                                                 'loss': ['linear', 'square', 'exponential']}, 'R'),
    'GBR': (GradientBoostingRegressor(random_state=0),
            {'n_estimators': randint(10, 500), 'learning_rate': uniform(0.05, 2.0), 'max_depth': randint(1, 50),
             'min_samples_split': randint(2, 50), 'min_samples_leaf': randint(1, 50),
             'min_weight_fraction_leaf': uniform(0.0, 0.5), 'max_leaf_nodes': randint(2, 50),
             'subsample': uniform(0.0, 0.9), 'alpha': uniform(0.0, 1.0)}, 'R'),
    'LinearSVR': (LinearSVR(random_state=0),
                  {'C': uniform(0.1, 1.5), 'loss': ['epsilon_insensitive', 'squared_epsilon_insensitive'],
                   'epsilon': uniform(0.0, 1.0), 'tol': uniform(0.00005, 0.005), 'fit_intercept': [True, False]}, 'R'),
    # 'SVR'      : ( SVR(max_iter=1000), {'C': uniform(0.1, 1.5), 'epsilon': uniform(0, 1.0), 'kernel': ['poly', 'rbf', 'sigmoid'], 'degree': randint(2, 5), 'coef0': uniform(0.0, 0.1), 'shrinking': [True, False], 'tol': uniform(0.0005, 0.005)}, 'R' ),
    'SVR': (SVR(), {'C': uniform(0.1, 1.5), 'epsilon': uniform(0, 1.0), 'kernel': ['poly', 'rbf', 'sigmoid'],
                    'degree': randint(2, 5), 'coef0': uniform(0.0, 0.1), 'shrinking': [True, False],
                    'tol': uniform(0.0005, 0.005)}, 'R'),
}
user_item_data_structure = []

"""
with open(svmlight_files_path.joinpath("HR-all-train.merged"), 'r') as file:
    lines = file.readlines()
    for line in lines:
        #print("\n", line)
        splitted_line = line.split('\t')
        print("splitted line: \n", splitted_line)
        user_item = splitted_line[0]
        features = splitted_line[1]

"""

"""
Colocar dentro da estrutura de hibridização (código e UML)
menção a métodos como build_features e process_features

-> Além disso, mudar nome do repositório para o RecSysExp
-> Generalizar texto para fazer menção
-> rodar FLWS e STREAM para todos os folds
-> submeter o resultado deles as métricas
-> Comparar resultados
-> Gerar visualizações para o

"""

test_features, test_outs = load_svmlight_file(
    svmlight_files_path.joinpath("HR-all-test.skl")
)
train_features, train_outs = load_svmlight_file(
    svmlight_files_path.joinpath("HR-all-train.skl")
)

# Utility function to report best scores
def report(search):
    print(f"\t\t- Best score: {search.best_score_:.6f}")
    print(f"\t\t- Parameters: {search.best_params_}\n")
"""

"""
if __name__ == '__main__':
    st = time.time()
    print("\nStarted")
    print(datetime.now())
    n_iter_search = 100
    cv = 5
    strategy = 'G'
    for alg in algorithms.keys():
        print("--------------\n")
        print('- Algorithm: ' + alg)
        print("..............\n")
        start = time.time()
        TrainFeatures, TrainOuts = load_svmlight_file(svmlight_files_path.joinpath("HR-all-train.skl"))
        # TrainFeatures = TrainFeatures.fillna(0) # Problem with NaN, using ZERO
        print("\t\t- Training took\t%.2f\tseconds." % (time.time() - start))
        start = time.time()
        print("alg[1]: ", algorithms[alg][1])
        if strategy == 'G':
            search = GridSearchCV(algorithms[alg][0], param_grid=algorithms[alg][1])
        else:
            search = RandomizedSearchCV(algorithms[alg][0], param_distributions=algorithms[alg][1], cv=cv,
                                        n_iter=n_iter_search, n_jobs=-1)

        search.fit(TrainFeatures.toarray(), TrainOuts)

        print("\t\t- RandomizedSearchCV took\t%.2f\tseconds\tfor %d candidates parameter settings." % (
            (time.time() - start), n_iter_search))

        report(search)

    et = time.time()
    ds = et - st
    dm = ds / 60
    print("==============\n")
    print("Finished in %2.2f sec / %2.2f min (EXE time)." % (ds, dm))
    print(datetime.now())
