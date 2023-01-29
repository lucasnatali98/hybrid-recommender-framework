import pandas as pd
from sklearn.model_selection import train_test_split
from src.preprocessing.preprocessing import AbstractPreProcessing
from pandas import DataFrame
from src.data.loader import Loader
from src.utils import hrf_experiment_output_path, process_parameters

class SplitProcessing(AbstractPreProcessing):
    def __init__(self, parameters: dict):
        super().__init__()
        default_keys = {
            'test_size',
            'train_size',
            'random_state'
        }
        parameters = process_parameters(parameters, default_keys)
        self.target = parameters.get('target')
        self.test_size = parameters.get('test_size')
        self.train_size = parameters.get('train_size')
        self.random_state = parameters.get('random_state')
        self.shuffle = parameters.get('shuffle')
        self.stratify = parameters.get('stratify')



    def pre_processing(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
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

        new_dfs = {
            'x_train': X_train,
            'x_test': X_test,
            'y_train': y_train,
            'y_test': y_test
        }

        self._save_splited_dataset(new_dfs)
        return data

    def _save_splited_dataset(self, splitted_dataframes: dict) -> None:
        """
        Função responsável por fazer o armazenamento dentro da saída do experimento das divisões feitas
        no dataframe original

        @param split_processing:
        @return: None
        """
        loader = Loader()
        preprocessing_experiment_output_path = hrf_experiment_output_path().joinpath("preprocessing/")
        for key, value in splitted_dataframes.items():
            if key == 'x_train':
                loader.convert_to("csv", value, preprocessing_experiment_output_path.joinpath("xtrain.csv"))
            if key == 'x_test':
                loader.convert_to("csv", value, preprocessing_experiment_output_path.joinpath("xtest.csv"))
            if key == 'y_train':
                loader.convert_to("csv", value, preprocessing_experiment_output_path.joinpath("ytrain.csv"))
            if key == 'y_test':
                loader.convert_to("csv", value, preprocessing_experiment_output_path.joinpath('ytest.csv'))
