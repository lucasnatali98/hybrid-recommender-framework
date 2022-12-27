from sklearn.model_selection import train_test_split
from src.preprocessing.preprocessing import AbstractPreProcessing
from pandas import DataFrame
from src.data.loader import Loader
from src.utils import hrf_experiment_output_path, process_parameters

class SplitProcessing(AbstractPreProcessing):
    def __init__(self, parameters: dict):
        """
        
        """
        super().__init__()
        default_keys = {
            'test_size',
            'train_size',
            'random_state'
        }
        parameters = process_parameters(parameters, default_keys)
        self.test_size = parameters['test_size']
        self.train_size = parameters['train_size']
        self.random_state = parameters['random_state']
        self.shuffle = parameters['shuffle']
        self.stratify = parameters['stratify']



    def pre_processing(self, data, **kwargs):
        """

        @param **kwargs:
        @param data:
        @return:
        """
        y = data['rating']
        X = data.drop(columns=['rating'], axis=1)

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            train_size=self.train_size,
            test_size=self.test_size,
            random_state=self.random_state,
            shuffle=self.shuffle,
            stratify=None)

        # return X_train, X_test, y_train, y_test
        new_dfs = {
            'x_train': X_train,
            'x_test': X_test,
            'y_train': y_train,
            'y_test': y_test
        }

        self._save_splited_dataset(new_dfs)
        return data

    def row_based_splitting(self, data: DataFrame, partitions: int, rng_spec):
        """


        @return:
        """
        pass

    def user_based_splitting(self):
        pass

    def _save_splited_dataset(self, split_processing: dict):
        """

        @param split_processing:
        @return:
        """
        loader = Loader()
        preprocessing_experiment_output_path = hrf_experiment_output_path().joinpath("preprocessing/")
        print("Preprocessing experiment output path: ", preprocessing_experiment_output_path)
        for key, value in split_processing.items():
            if key == 'x_train':
                loader.convert_to("csv", value, preprocessing_experiment_output_path.joinpath("xtrain.csv"))
            if key == 'x_test':
                loader.convert_to("csv", value, preprocessing_experiment_output_path.joinpath("xtest.csv"))
            if key == 'y_train':
                loader.convert_to("csv", value, preprocessing_experiment_output_path.joinpath("ytrain.csv"))
            if key == 'y_test':
                loader.convert_to("csv", value, preprocessing_experiment_output_path.joinpath('ytest.csv'))
