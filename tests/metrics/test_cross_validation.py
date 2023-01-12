from src.metrics.cross_validation import CrossValidation
from src.recommenders.item_knn import ItemKNN
from sklearn.metrics import ndcg_score, mean_squared_error, mean_absolute_error, make_scorer
import pandas as pd
from src.utils import hrf_experiment_output_path


parameters_item_knn = {
    "maxNumberNeighbors": 20,
    "minNumberNeighbors": 4,
    "saveNeighbors": 6.0,
    "feedback": "implicit",
    "aggregate": "weighted-average",
    "use_ratings": True
}
algorithm = ItemKNN(parameters_item_knn)
fold_path = hrf_experiment_output_path().joinpath("preprocessing/folds/train/train-fold-1.csv")
train_fold_1 = pd.read_csv(fold_path, index_col=[0])
print(train_fold_1)
X = train_fold_1.drop(columns=['rating'])
y = train_fold_1['rating']

ndcg_scorer = make_scorer(ndcg_score)
rmse_scorer = make_scorer(mean_absolute_error)

metrics = {
    'rmse': rmse_scorer,
    'ndcg': ndcg_scorer
}

parameters_cross_validation = {
    "lib": "sklearn",
    "metrics": metrics,
    "algorithm": algorithm,
    "X": X,
    "y": y,
    "cv": None,
    "return_train_score": False,
    "return_estimator": False,
    "error_score": True
}
cross_validation = CrossValidation(parameters_cross_validation)


class TestCrossValidation:

    def test_evaluation_sklearn(self):

        scores = cross_validation.evaluation_sklearn()
        print("scores: ", scores)
