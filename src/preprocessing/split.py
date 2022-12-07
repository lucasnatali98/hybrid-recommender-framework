from sklearn.model_selection import train_test_split
from src.preprocessing.preprocessing import AbstractPreProcessing
from pandas import DataFrame



class SplitProcessing(AbstractPreProcessing):
    def __init__(self, parameters: dict):
        """
        
        """
        super().__init__()
        self.test_size = parameters['test_size']
        self.train_size = parameters['train_size']
        self.random_state = parameters['random_state']
        self.shuffle = parameters['shuffle']
        self.stratify = parameters['stratify']


    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """


        default_keys = [
            'test_size',
            'train_size',
            'random_state'
        ]
        parameters_keys = parameters.keys()

        for key in default_keys:
            if key not in parameters_keys:
                raise KeyError("A chave obrigatória {} não foi informada no arquivo de configuração".format(key))

        return parameters

    def pre_processing(self, data, **kwargs):
        """

        @param **kwargs:
        @param data:
        @return:
        """
        y = data['rating']
        X = data.drop(columns = ['rating'], axis=1)

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            train_size=self.train_size,
            test_size=self.test_size,
            random_state=self.random_state,
            shuffle=self.shuffle,
            stratify=None)

        #return X_train, X_test, y_train, y_test
        return {
            'x_train': X_train,
            'x_test': X_test,
            'y_train': y_train,
            'y_test': y_test
        }

    def row_based_splitting(self, data: DataFrame, partitions: int, rng_spec):
        """


        @return:
        """
        pass

    def user_based_splitting(self):
        pass



