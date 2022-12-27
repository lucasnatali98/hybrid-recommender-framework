from src.metrics.metric import PredictionMetric
import lenskit.metrics.predict as lenskit_predict


class RMSE(PredictionMetric):
    """


    """

    def __init__(self, parameters: dict) -> None:
        """
        
        """
        pass

    def evaluate(self, predictions, truth):
        """

        @param predictions:
        @param truth:
        @return:
        """
        pass

    def check_missing(self, truth, missing):
        """

        @param truth:
        @param missing:
        @return:
        """
        pass

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters:
        @return:
        """
        default_keys = {

        }
        parameters_keys_list = list(parameters.keys())

        parameters_keys = set()
        for parameter in parameters_keys_list:
            parameters_keys.add(parameter)

        if default_keys.issubset(parameters_keys):
            pass
        else:
            raise KeyError("Você não informou uma das chaves obrigatorias")


class RMSELensKit(PredictionMetric):


    def __init__(self):
        pass

    def evaluate(self, predictions, truth):
        """

        @param predictions:
        @param truth:
        @return:
        """
        return lenskit_predict.rmse(predictions=predictions, truth=truth, missing='error')

    def check_missing(self, truth, missing):
        """
            Check for missing truth values.
            Args:
                truth: the series of truth values
                missing: what to do with missing values
            """
        if missing == 'error' and truth.isna().any():
            missing = truth.isna().sum()
            raise ValueError('missing truth for {} predictions'.format(missing))
