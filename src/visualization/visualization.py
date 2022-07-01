from abc import ABC, abstractmethod

class Visualization(ABC):
    @abstractmethod
    def parse(self, obj):
        """
        
        """
        pass
    
    @abstractmethod
    def plot(self):
        """
        
        """
        pass


class AbstractVisualization(Visualization):

    def parse(self, obj):
        """
        
        """
        pass

    def plot(self):
        """
        
        """
        pass

class TablePlot(AbstractVisualization):
    def parse(self, obj):
        """
        
        """
        pass
    def plot(self):
        """
        
        """
        pass

class StaticPlot(AbstractVisualization):
    def parse(self, obj):
        """
        
        """
        pass
    def plot(self):
        """
        
        """
        pass

class InteractivePlot(AbstractVisualization):
    def parse(self, obj):
        """
        
        """
        pass
    def plot(self):
        """
        
        """
        pass