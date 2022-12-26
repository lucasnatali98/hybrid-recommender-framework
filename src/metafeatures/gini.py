
from src.metafeatures.metafeature import ColaborativeMetaFeature


class Gini(ColaborativeMetaFeature):
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

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters:
        @return:
        """
        default_keys = set()
        parameters_keys_list = list(parameters.keys())

        parameters_keys = set()
        for parameter in parameters_keys_list:
            parameters_keys.add(parameter)

        if default_keys.issubset(parameters_keys):
            pass
        else:
            raise KeyError("Você não informou uma das chaves obrigatorias")

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