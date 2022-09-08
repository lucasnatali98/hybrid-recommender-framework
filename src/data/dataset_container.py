from src.shared.container import Container
from src.data.factory import DatasetFactory


class DatasetContainer(Container):
    """

    """
    def __init__(self, parameters: dict):
        """


        """
        super().__init__()
        datasets = parameters['datasets']

        if len(datasets) == 0:
            self.dataset_objects = []
        else:
            self.recommenders_object = []
            self.dataset_factory = DatasetFactory(parameters)
            self.dataset_objects = self.dataset_factory.create
