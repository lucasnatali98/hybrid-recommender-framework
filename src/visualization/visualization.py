from abc import ABC, abstractmethod

class Visualization(ABC):
    
    @abstractmethod
    def plot(self):
        """

        @return:
        """
        raise Exception("O método plot de Visualization não está implementado")


class AbstractVisualization(Visualization):

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param obj:
        @return:
        """
        pass

    def plot(self):
        """

        @return:
        """
        pass

class TablePlot(AbstractVisualization):
    def parse(self, obj):
        """

        @param obj:
        @return:
        """
        pass
    def plot(self):
        """

        @return:
        """
        pass

class StaticPlot(AbstractVisualization):
    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters:
        @return:
        """
        pass
    def plot(self):
        """

        @return:
        """
        pass

class InteractivePlot(AbstractVisualization):
    def process_parameters(self, parameters: dict) -> dict:
        """

        @param obj:
        @return:
        """
        pass
    def plot(self):
        """

        @return:
        """
        pass