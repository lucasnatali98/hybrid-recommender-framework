from sklearn.model_selection import cross_validate as cross_validate_sklearn
from surprise.model_selection import cross_validate as cross_validate_surprise
from sklearn.model_selection import cross_val_score
from src.utils import process_parameters
class CrossValidation:

    def __init__(self, parameters: dict) -> None:
        """

        @param parameters:
        """
        default_keys = set()
        parameters = self.process_parameters(parameters, default_keys)
        self.lib = parameters['lib']
        self.metrics = parameters['metrics']
        self.algorithm = parameters['algorithm']
        self.X = parameters['x']
        self.y = parameters['y']
        self.cv = parameters['cv']
        self.return_train_score = parameters['return_train_score']
        self.return_estimator = parameters['return_estimator']
        self.error_score = parameters['error_score']

    def evaluation_surprise(self):
        """

        @return:
        """
        pass
    def evaluation_sklearn(self):
        """

        @return:
        """
        scores = cross_validate_sklearn(
            estimator=self.algorithm,
            X=self.X,
            y=self.y,
            scoring=self.metrics
        )
        return scores



