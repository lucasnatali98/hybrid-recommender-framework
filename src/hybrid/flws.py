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
from operator import itemgetter


class FLWS(HybridWeighted):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        super().__init__(parameters)
        default_keys = set()
        self.linear_model = LinearRegression()
        self.algorithms = None
        self.weights = None
        self.mf_weights = None
        parameters = process_parameters(parameters, default_keys)

    def combine_metafeature_with_predictions(self, metafeatures: DataFrame, predictions: DataFrame) -> DataFrame:

        result_dataframe = predictions.copy()

        for metafeature in metafeatures:
            for mf_key, mf_value in metafeature.items():
                if re.search('item_user', mf_key) is not None:
                    metafeature_df = mf_value

                    mf_column_name = str(mf_key) + "_value"
                    metafeature_df = metafeature_df.rename(columns={
                        "valor": mf_column_name
                    })
                    result_dataframe = merge(result_dataframe, metafeature_df, on=[
                        'item',
                        'user'
                    ])

        return result_dataframe

    def set_weights(self, weights):
        self.weights = weights

    def metafeatures_weitghts(self, mf_weights):
        self.mf_weights = mf_weights

    def predict(self, metafeatures, predictions):

        pass

    def run(self, algorithm_predictions_df: DataFrame) -> DataFrame:
        """

        @return:
        """
        hybrid_result = []
        temp_array = []
        predictions = []

        for row in algorithm_predictions_df.itertuples():
            result = row.prediction * row.gini_item_user_value * row.pearson_item_user_value * row.proportion_ratings_item_user_value
            temp_array.append([
                row.gini_item_user_value,
                row.pearson_item_user_value,
                row.proportion_ratings_item_user_value
            ])
            predictions.append(row.prediction)

        temp_array = np.array(temp_array)
        # temp_array = np.array(temp_array).reshape(-1,1)
        print("temp array shape: ", len(temp_array))
        print("predictions length: ", len(predictions))

        self.linear_model.fit(temp_array, predictions)
        score = self.linear_model.score(temp_array, predictions)
        print("Score of linear model: ", score)
        print("Coeficients of linear model: ", self.linear_model.coef_)

        return algorithm_predictions_df


flws = FLWS({
    "x": True
})


collaborative_mf_path = hrf_metafeatures_path().joinpath("collaborative")

predict_result_item_knn = read_csv(rec_temp_files_path.joinpath(
    "ItemKNN-predict-result-100k.csv"
), index_col=[0])
predict_result_user_knn = read_csv(rec_temp_files_path.joinpath(
    "UserKNN-predict-result-100k.csv"
), index_col=[0])
predict_result_bias = read_csv(rec_temp_files_path.joinpath(
    "bias-predict-result-100k.csv"
), index_col=[0])
predict_result_biased_svd = read_csv(rec_temp_files_path.joinpath(
    "biasedSVD-predict-result-100k.csv"
), index_col=[0])

const_rec = {
    "item_knn": predict_result_item_knn,
    "user_knn": predict_result_user_knn,
    "bias": predict_result_bias,
    "biasedSVD": predict_result_biased_svd

}

metafeatures = read_metafeatures_textfiles()
cf_metafeatures = metafeatures.get('collaborative')
cb_metafeatures = metafeatures.get('content-based')

gini_item = None
gini_item_user = None
gini_user = None
person_item = None
person_item_user = None
person_user = None
proportion_ratings_user = None
proportion_ratings_item_user = None
proportion_ratings_item = None

for cfm in cf_metafeatures:
    for key, value in cfm.items():
        if key == "Gini_Item":
            gini_item = value
        if key == "Gini_ItemUser":
            gini_item_user = value
        if key == "Gini_User":
            gini_user = value
        if key == "Pearson_Item":
            person_item = value
        if key == "Pearson_User":
            person_user = value
        if key == "Pearson_ItemUser":
            person_item_user = value
        if key == "PR_Item":
            proportion_ratings_item = value
        if key == "PR_ItemUser":
            proportion_ratings_item_user = value
        if key == "PR_User":
            proportion_ratings_user = value

mf_weights = {
    'gini_user': 1,
    'gini_item_user': 2,
    'gini_item': 3,
    'pearson_user': 4,
    'pearson_item_user': 6,
    'pearson_item': 7,
    'proportion_ratings_user': 2,
    'proportion_ratings_item_user': 1,
    'proportion_ratings_item': 1
}
flws.mf_weights = mf_weights

flws.add_metafeature({"gini_user": gini_user})
flws.add_metafeature({"gini_item_user": gini_item_user})
flws.add_metafeature({"gini_item": gini_item})
flws.add_metafeature({"pearson_user": person_user})
flws.add_metafeature({"pearson_item_user": person_item_user})
flws.add_metafeature({"pearson_item": person_item})
flws.add_metafeature({"proportion_ratings_user": proportion_ratings_user})
flws.add_metafeature({"proportion_ratings_item_user": proportion_ratings_item_user})
flws.add_metafeature({"proportion_ratings_item": proportion_ratings_item})

flws.algorithms = const_rec
# fwls.add_constituent(const_rec)

flws.set_weights({
    "item_knn": 4,
    "user_knn": 2,
    "bias": 2.5,
    "biasedSVD": 1.0
})
# print(fwls.metafeatures)
result_df = flws.combine_metafeature_with_predictions(flws.metafeatures, const_rec.get('bias'))
