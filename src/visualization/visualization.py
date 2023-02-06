from abc import ABC, abstractmethod
from pandas import DataFrame


class Visualization(ABC):

    @abstractmethod
    def plot(self, data: DataFrame = None, **kwargs):
        """

        @return:
        """
        pass


class AbstractVisualization(Visualization):

    @abstractmethod
    def plot(self, data: DataFrame = None, **kwargs):
        """

        @return:
        """
        pass


class TablePlot(AbstractVisualization):

    @abstractmethod
    def plot(self, data: DataFrame = None, **kwargs):
        """

        @return:
        """
        pass


class StaticPlot(AbstractVisualization):

    @abstractmethod
    def plot(self, data: DataFrame = None, **kwargs):
        """

        @return:
        """
        pass


class InteractivePlot(AbstractVisualization):
    @abstractmethod
    def plot(self, data: DataFrame = None, **kwargs):
        """

        @return:
        """
        pass
