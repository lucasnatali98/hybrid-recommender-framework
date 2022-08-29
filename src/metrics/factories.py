from abc import abstractmethod

from src.metrics.metric import Metric

from src.metrics.ndcg import NDCG
from src.metrics.mae import MAE
from src.metrics.recall import Recall
from src.metrics.rmse import RMSE
from src.metrics.epd import EPD


class Creator:

    @abstractmethod
    def create(self) -> Metric:
        pass


class EPDFactory(Creator):
    def __init__(self):
        pass

    def create(self) -> Metric:
        """

        @return:
        """
        return EPD()


class MAEFactory(Creator):
    def __init__(self):
        pass

    def create(self) -> Metric:
        """

        @return:
        """
        return MAE()


class RecallFactory(Creator):
    def __init__(self):
        pass

    def create(self) -> Metric:
        """

        @param self:
        @return:
        """
        return Recall()


class RMSEFactory(Creator):
    def __init__(self):
        pass

    def create(self) -> Metric:
        """

        @return:
        """

        return RMSE()


class NDCGFactory(Creator):
    def __init__(self):
        pass

    def create(self) -> Metric:
        """

        @return:
        """

        return NDCG()