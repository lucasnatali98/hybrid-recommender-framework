from abc import ABC, abstractmethod

class MetaFeature(ABC):

    @abstractmethod
    def fit(self):
        """
        
        """

        raise Exception("O método fit de MetaFeature não está implementado")

    @abstractmethod
    def predict(self):
        """
        
        """
        raise Exception("O método predict de MetaFeature não está implementado")

    @abstractmethod
    def update(self):
        """
        
        """
        raise Exception("O método update de MetaFeature não está implementado")




class ColaborativeMetaFeature(MetaFeature):

    @abstractmethod
    def fit(self):
        """
        
        """
        pass
    @abstractmethod
    def predict(self):
        """
        
        """
        pass
    @abstractmethod
    def update(self, obj):
        """
        
        """
        pass

class ContentBasedMetaFeature(MetaFeature):
    @abstractmethod
    def fit(self):
        """
        
        """
        pass
    @abstractmethod
    def predict(self):
        """
        
        """
        pass
    @abstractmethod
    def update(self, obj):
        """
        
        """
        pass