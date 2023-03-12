import pandas as pd
from lenskit.metrics.topn import precision, recall
from src.metrics.rmse import LenskitRMSE
from src.metrics.mae import LenskitMAE
from src.metrics.ndcg import LenskitNDCG
from src.metrics.dcg import LenskitDCG

from src.utils import hrf_experiment_output_path
from src.data.movielens import MovieLens

rec_temp_files_path = hrf_experiment_output_path().joinpath("rec_temp_files")

evaluate_predict_process_100k = {
    "100k": {
        "prediction_files": {
            "bias": "bias-predict-result-100k.csv",
            "biasedSVD": "biasedSVD-predict-result-100k.csv",
            "ItemKNN": "ItemKNN-predict-result-100k.csv",
            "UserKNN": "UserKNN-predict-result-100k.csv"
        },
        "recommendation_files": {
            "bias": "bias-recommend-result-100k.csv",
            "biasedSVD": "biasedSVD-recommend-result-100k.csv",
            "ItemKNN": "ItemKNN-recommend-result-100k.csv",
            "UserKNN": "UserKNN-recommend-result-100k.csv"
        }
    }
}

evaluate_predict_process = {
    "200k": {
        "prediction_files": {
            "bias": "bias-predict-result-200k.csv",
            "biasedSVD": "biasedSVD-predict-result-200k.csv",
            "ItemKNN": "ItemKNN-predict-result-200k.csv",
            "UserKNN": "UserKNN-predict-result-200k.csv"
        },
        "recommendation_files": {
            "bias": "bias-recommend-result-200k.csv",
            "biasedSVD": "biasedSVD-recommend-result-200k.csv",
            "ItemKNN": "ItemKNN-recommend-result-200k.csv",
            "UserKNN": "UserKNN-recommend-result-200k.csv"
        }
    },
    "300k": {
        "prediction_files": {
            "bias": "bias-predict-result-300k.csv",
            "biasedSVD": "biasedSVD-predict-result-300k.csv",
            "ItemKNN": "ItemKNN-predict-result-300k.csv",
            "UserKNN": "UserKNN-predict-result-300k.csv"
        },
        "recommendation_files": {
            "bias": "bias-recommend-result-300k.csv",
            "biasedSVD": "biasedSVD-recommend-result-300k.csv",
            "ItemKNN": "ItemKNN-recommend-result-300k.csv",
            "UserKNN": "UserKNN-recommend-result-300k.csv"
        }
    },
    "400k": {
        "prediction_files": {
            "bias": "bias-predict-result-400k.csv",
            "biasedSVD": "biasedSVD-predict-result-400k.csv",
            "ItemKNN": "ItemKNN-predict-result-400k.csv",
            "UserKNN": "UserKNN-predict-result-400k.csv"
        },
        "recommendation_files": {
            "bias": "bias-recommend-result-400k.csv",
            "biasedSVD": "biasedSVD-recommend-result-400k.csv",
            "ItemKNN": "ItemKNN-recommend-result-400k.csv",
            "UserKNN": "UserKNN-recommend-result-400k.csv"
        }
    }
}

ratings = MovieLens({
    'proportion': 'ml-latest-small'
}).ratings



truth = ratings['rating']
truth_recs = ratings

truth_for_samples = pd.read_csv(
    rec_temp_files_path.joinpath(
        "ratings-400k.csv"
    ))

print(truth_for_samples['rating'])

def evaluate_process_other_databases(evaluate_obj: dict):
    evaluate_result = {}
    for key in evaluate_obj.keys():
        obj: dict = evaluate_obj.get(key)
        for key2, value in obj.items():
            if key2 == "prediction_files":
                predictions_obj = value
                for algorithm, path in predictions_obj.items():
                    predictions = pd.read_csv(
                        rec_temp_files_path.joinpath(path),
                        index_col=[0]
                    )
                    preds = predictions['prediction']

                    evaluate_result[key] = {
                        algorithm: {
                            "rmse": measure_predictions(preds, truth, "rmse"),
                            "mae": measure_predictions(preds, truth, "mae"),
                            "precision": precision(predictions, truth),
                            "recall": recall(predictions, truth)
                        }
                    }

            if key2 == "recommendation_files":
                predictions_obj = value
                for algorithm, path in predictions_obj.items():
                    recs = pd.read_csv(
                        rec_temp_files_path.joinpath(path),
                        index_col=[0]
                    )

                    hasKey = evaluate_result[key].get(algorithm, None)

                    if hasKey is None:
                        evaluate_result[key].setdefault({
                            algorithm: {
                                "ndcg": measure_predictions(recs, truth_recs, "ndcg"),
                                "dcg": measure_predictions(recs, truth_recs, "dcg")
                            }
                        })

                    else:
                        evaluate_result[key].update({
                            algorithm: {
                                "ndcg": measure_predictions(recs, truth_recs, "ndcg"),
                                "dcg": measure_predictions(recs, truth_recs, "dcg")
                            }
                        })


    return evaluate_result


def evaluate_process_100k(evaluate_obj: dict):


    evaluate_result = {}
    e100k = evaluate_obj.get('400k')
    for key, value in e100k.items():
        if key == "prediction_files":
            predictions_obj = value
            for algorithm, path in predictions_obj.items():

                predictions = pd.read_csv(
                    rec_temp_files_path.joinpath(path)
                )
                preds = predictions['prediction']

                evaluate_result[algorithm] = {
                    "rmse": measure_predictions(preds, truth_for_samples['rating'], "rmse"),
                    "mae": measure_predictions(preds, truth_for_samples['rating'], "mae"),
                    "precision": precision(predictions, truth_for_samples['rating']),
                    "recall": recall(predictions, truth_for_samples['rating'])
                }

        if key == "recommendation_files":
            predictions_obj = value
            for algorithm, path in predictions_obj.items():
                recs = pd.read_csv(
                    rec_temp_files_path.joinpath(path),
                    index_col=[0]
                )

                evaluate_result[algorithm].update({
                    "ndcg": measure_predictions(recs, truth_for_samples, "ndcg"),
                    "dcg": measure_predictions(recs, truth_for_samples, "dcg")
                })

    return evaluate_result


def measure_predictions(prediction_df, truth, metric):
    measure_result = {}

    evaluator = None
    if metric == "rmse":
        evaluator = LenskitRMSE({})
    if metric == "mae":
        evaluator = LenskitMAE({})
    if metric == "ndcg":
        evaluator = LenskitNDCG({})
    if metric == "dcg":
        evaluator = LenskitDCG({})

    return evaluator.evaluate(prediction_df, truth)

result = evaluate_process_100k(evaluate_predict_process)
result = pd.DataFrame(result)
print(result)

"""

result = evaluate_process_other_databases(evaluate_predict_process)
e200k = result.get('200k', None)
e300k = result.get('300k', None)
e400k = result.get('400k', None)

e200k = pd.DataFrame(e200k)
e300k = pd.DataFrame(e300k)
e400k = pd.DataFrame(e400k)

print(e200k)
print(e300k)
print(e400k)


"""
