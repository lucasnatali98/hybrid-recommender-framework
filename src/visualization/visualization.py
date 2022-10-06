from abc import ABC, abstractmethod

class Visualization(ABC):
    @abstractmethod
    def parse(self, obj):
        """

        @param obj:
        @return:
        """
        pass
    
    @abstractmethod
    def plot(self):
        """

        @return:
        """
        pass


class AbstractVisualization(Visualization):

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

class InteractivePlot(AbstractVisualization):
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