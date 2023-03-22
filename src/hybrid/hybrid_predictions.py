
from pandas import DataFrame, Series, read_csv, merge

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
from operator import itemgetter
from sklearn.metrics import recall_score, mean_squared_error, mean_absolute_error
from src.utils import hrf_experiment_output_path
rec_temp_files_path = hrf_experiment_output_path().joinpath("rec_temp_files")
svmlight_files_path = hrf_experiment_output_path().joinpath("svmlight_files")

fwls_output_path = hrf_experiment_output_path().joinpath("hybrid/fwls")
stream_output_path = hrf_experiment_output_path().joinpath("hybrid/stream")

algorithms = {
    "Ridge": Ridge(),
    'B-Ridge': BayesianRidge(),
    'LinearSVR': LinearSVR(random_state=0),
    'GBR': GradientBoostingRegressor(n_estimators=100,random_state=0),
    'RFR': RandomForestRegressor(n_estimators=100, n_jobs=-1, random_state=0, bootstrap=True),
    'SGD': SGDRegressor(),
    'AdaBoost': AdaBoostRegressor(n_estimators=100)

}
folds = [
    'F1234-5',
    'F1235-4',
    'F1245-3',
    'F1345-2',
    'F2345-1'
]


weighted_strategy = "STREAM"
if __name__ == '__main__':
    scores = {}

    for fold in folds:
        path_to_fold = svmlight_files_path.joinpath(fold)


        test_features, test_outs = load_svmlight_file(
            path_to_fold.joinpath("STREAM-all-test.skl")
        )

        train_features, train_outs = load_svmlight_file(
            path_to_fold.joinpath("STREAM-all-train.skl")
        )

        for algorithm_name, estimator in algorithms.items():

            estimator.fit(train_features.toarray(), train_outs)

            predictions = estimator.predict(test_features)
            predictions_serie = Series(predictions, name='predictions')

            path_to_predict_stream = stream_output_path.joinpath(fold)

            predictions_serie.to_csv(
                path_to_predict_stream.joinpath(algorithm_name + "_predictions.csv")
            )

            score = estimator.score(test_features, test_outs)

            print("Score: ", score)

            scores[algorithm_name] = score

            try:
                coef_series = Series(estimator.coef_, name='coef')

                coef_series.to_csv(
                    path_to_predict_stream.joinpath(algorithm_name + "_coef.csv")
                )

            except Exception as e:
                print(e)


            print("Scores: \n", scores)
            scores_df = DataFrame(scores, index=[0])
            score_path_result = stream_output_path.joinpath(fold)
            scores_df.to_csv(score_path_result.joinpath(algorithm_name + "_scores.csv"))