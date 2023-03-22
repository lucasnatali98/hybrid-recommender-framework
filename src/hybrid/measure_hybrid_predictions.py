from src.utils import hrf_experiment_output_path
import pandas as pd
stream_path = hrf_experiment_output_path().joinpath("hybrid/stream")
svm_lightfiles_path = hrf_experiment_output_path().joinpath("svmlight_files")

folds = [
    'F1234-5',
    'F1235-4',
    'F1245-3',
    'F1345-2',
    'F2345-1'
]
from sklearn.datasets import load_svmlight_file
import pandas as pd
from sklearn.metrics import mean_squared_error
test_features, test_outs = load_svmlight_file(svm_lightfiles_path.joinpath(folds[0]).joinpath('STREAM-all-test.skl'))

ada = pd.read_csv(stream_path.joinpath(folds[0]).joinpath('AdaBoost_predictions.csv'), index_col=[0])

print(ada)
print(test_outs)

print(mean_squared_error(test_outs, ada))