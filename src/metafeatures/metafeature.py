from abc import ABC, abstractmethod
from src.utils import process_parameters, hrf_metafeatures_path, check_if_directory_exists
from pandas import DataFrame, Series, read_csv
import os


def read_metafeatures_textfiles():
    result = {
        'collaborative': [],
        'contentbased': [],
    }
    collaborative_dir = hrf_metafeatures_path().joinpath("collaborative")
    contentbased_dir = hrf_metafeatures_path().joinpath("contentbased")

    print("collaborative dir: ", collaborative_dir)
    print("contentbased_dir: ", contentbased_dir)

    collaborative_dir_files = None
    contentbased_dir_files = None

    if check_if_directory_exists(collaborative_dir):
        collaborative_dir_files = os.listdir(collaborative_dir)
    if check_if_directory_exists(contentbased_dir):
        contentbased_dir_files = os.listdir(contentbased_dir)


    for collaborative_file in collaborative_dir_files:
        splitted_cf = collaborative_file.split("_") # Exemplo: cf_Gini_Item.txt
        cf_name = splitted_cf[1]
        mf_type = splitted_cf[2]
        mf_type = mf_type.split(".")[0]
        columns = None

        if mf_type == "Item":
            columns = ['item', 'value']
        if mf_type == "User":
            columns = ['user', 'value']
        if mf_type == "ItemUser":
            columns = ['user', 'item', 'value']

        mf_dataframe = {}
        file = collaborative_dir.joinpath(collaborative_file)

        df = read_csv(file, sep=';')

        mf_dataframe[cf_name + "_" + mf_type] = df
        result['collaborative'].append(mf_dataframe)



    for contentbased_file in contentbased_dir_files:
        splitted_cb = contentbased_file.split("_")  # Exemplo: cf_Gini_Item.txt
        cb_name = splitted_cb[1]
        mf_type = splitted_cb[2]
        mf_type = mf_type.split(".")[0]
        columns = None

        if mf_type == "Item":
            columns = ['item', 'value']
        if mf_type == "User":
            columns = ['user', 'value']
        if mf_type == "ItemUser":
            columns = ['user', 'item', 'value']

        mf_dataframe = {}
        file = contentbased_dir.joinpath(contentbased_file)
        df = read_csv(file, sep=';')
        print("content df: ", df)
        mf_dataframe[cb_name + "_" + mf_type] = df
        result['contentbased'].append(mf_dataframe)


    print(result)
    return result



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

        self.user = DataFrame(columns=['user', 'value'])
        self.userItem = DataFrame(columns=['user', 'item', 'value'])
        self.item = DataFrame(columns=['item', 'value'])



    def get_user_metafeature(self):
        pass
    def get_item_metafeature(self):
        pass

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



read_metafeatures_textfiles()