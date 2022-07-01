from abc import ABC, abstractmethod

class MetaFeature(ABC):

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
    def update(self):
        """
        
        """
        pass


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