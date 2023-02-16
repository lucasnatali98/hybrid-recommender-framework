from abc import ABC, abstractmethod
from src.utils import process_parameters


class MetaFeature(ABC):

    @abstractmethod
    def update(self, obj):
        """
        
        """
        pass


class AbstractMetaFeature(MetaFeature):
    """
    -> User
    -> UserItem
    -> Item

    -> Todos distintos (Preciso guardar e conseguir separamente cada calculo)

    """
    def __init__(self, parameters: dict) -> None:
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        self.buffer_size = parameters.get('bufferSize')
        self.use_text_output = parameters.get('useTextOutput', True)
        self.partition_length = parameters.get('partitionLength', 1)


    def update(self, obj):
        raise NotImplementedError

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

    def update(self, obj):
        raise NotImplementedError



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


    @abstractmethod
    def update(self, obj):
        raise NotImplementedError
