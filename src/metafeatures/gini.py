
from src.metafeatures.metafeature import ColaborativeMetaFeature
from src.utils import process_parameters


class Gini(ColaborativeMetaFeature):
    def __init__(self, parameters: dict) -> None:

        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        self.type = parameters.get('type')
        self.base_path = parameters.get('basePath')
        self.do_user = parameters.get('doUser')
        self.do_item = parameters.get('doItem')
        self.do_item_user = parameters.get('doItemUser')
        self.num_threads = parameters.get('numThreads')
        self.metric_parameter = parameters.get('metricParameter')
        self.fields = parameters.get('fields')
        self.items = parameters.get('items')


    def update(self, obj):
        """

        @param obj:
        @return:
        """
        pass