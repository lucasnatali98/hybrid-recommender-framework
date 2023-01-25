from abc import ABC, abstractmethod
from src.utils import process_parameters


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


class AbstractMetaFeature(MetaFeature):
    def __init__(self, parameters: dict) -> None:
        default_keys = {}
        parameters = process_parameters(parameters, default_keys)
        self.buffer_size = parameters.get('bufferSize')
        self.use_text_output = parameters.get('useTextOutput', True)
        self.partition_length = parameters.get('partitionLength', 1)

    def predict(self):
        pass

    def fit(self):
        pass

    def update(self):
        pass


class ColaborativeMetaFeature(MetaFeature):

    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        self.type = parameters.get('type', 'collaborative')
        self.base_path = parameters.get('basePath')
        self.do_user = parameters.get('doUser', True)
        self.do_item = parameters.get('doItem', True)
        self.do_item_user = parameters.get('doItemUser', True)
        self.num_threads = parameters.get('numThreads', 0)
        self.metric_parameter = parameters.get('metricParameter')
        self.fields = parameters.get('fields', [])
        self.items = parameters.get('items', [])

    def fit(self):
        """
        
        """
        pass

    def predict(self):
        """
        
        """
        pass

    def update(self, obj):
        """
        
        """
        pass


class ContentBasedMetaFeature(MetaFeature):

    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        self.type = parameters.get('type', 'content-based')
        self.index = parameters.get('index', False)
        self.index_folder = parameters.get('indexFolder', None)
        self.resource_file = parameters.get('resourceFile', None)
        self.separator_character = parameters.get('separatorCharacter', None)
        self.user_first_line_as_title = parameters.get('userFirstLineAsTitle', 0)
        self.user_preference_threshold = parameters.get('userPreferenceThreshold', 0)
        self.user_preference_file = parameters.get('userPreferenceFile', None)
        self.output_folder = parameters.get('outputFolder', None)
        self.base_path = parameters.get('basePath')
        self.do_user = parameters.get('doUser', True)
        self.do_item = parameters.get('doItem', True)
        self.do_item_user = parameters.get('doItemUser', True)
        self.num_threads = parameters.get('numThreads', 0)
        self.metric_parameter = parameters.get('metricParameter')
        self.fields = parameters.get('fields', [])
        self.items = parameters.get('items', [])

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
