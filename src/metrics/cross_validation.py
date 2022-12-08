from sklearn.model_selection import cross_validate as cross_validate_sklearn
from surprise.model_selection import cross_validate as cross_validate_surprise
class CrossValidation:
    """

    """
    def __init__(self, parameters: dict) -> None:
        """

        @param parameters:
        """
        parameters = self.process_parameters(parameters)
        self.lib = parameters['lib']
        self.metrics = parameters['metrics']
        self.algorithm = parameters['algorithm']
        self.X = parameters['x']
        self.y = parameters['y']
        self.cv = parameters['cv']
        self.return_train_score = parameters['return_train_score']
        self.return_estimator = parameters['return_estimator']
        self.error_score = parameters['error_score']


    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters:
        @return:
        """

        default_keys = [
            'metrics',
            'algorithm',
            'x',
            'y',
            'lib'
        ]
        for key in default_keys:
            if key not in parameters.keys():
                raise KeyError("A chave obrigatória {} não foi informada no arquivo de configuração".format(key))

        return parameters


    def evaluation_surprise(self):
        """

        @return:
        """
        pass
    def evaluation(self):
        """

        @return:
        """
        pass



