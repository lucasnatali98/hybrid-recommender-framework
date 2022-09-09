from src.shared.container import Container
from src.data.factory import DatasetFactory


class DatasetContainer(Container):
    """

    """
    def __init__(self, parameters: dict) -> None:
        """


        """
        super().__init__()
        datasets = parameters['instances']


        if len(datasets) == 0:
            pass
        else:
            self.dataset_factory = DatasetFactory(parameters)
            self.insert(0, self.dataset_factory.create)
