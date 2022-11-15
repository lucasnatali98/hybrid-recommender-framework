
from src.metafeatures.metafeature import ContentBasedMetaFeature


class Jaccard(ContentBasedMetaFeature):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        self.type = parameters['type']
        self.base_path = parameters['basePath']
        self.do_user = parameters['doUser']
        self.do_item = parameters['doItem']
        self.do_item_user = parameters['doItemUser']
        self.num_threads = parameters['numThreads']
        self.metric_parameter = parameters['metricParameter']
        self.fields = parameters['fields']
        self.items = parameters['items']

    def fit(self):
        """

        @return:
        """
        pass

    def predict(self):
        """

        @return:
        """
        pass

    def update(self, obj):
        """

        @param obj:
        @return:
        """
        pass