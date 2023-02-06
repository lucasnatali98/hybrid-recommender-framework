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
        parameters = process_parameters(parameters, default_keys)
        self.lib = parameters.get('lib')
        self.metrics = parameters.get('metrics')
        self.algorithm = parameters.get('algorithm')
        self.X = parameters.get('X')
        self.y = parameters.get('y')
        self.cv = parameters.get('cv')
        self.return_train_score = parameters.get('return_train_score')
        self.return_estimator = parameters.get('return_estimator')
        self.error_score = parameters.get('error_score')

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
