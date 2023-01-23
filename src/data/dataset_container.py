from src.shared.container import Container
from src.shared.generic_factory import GenericFactory

class DatasetContainer(Container):
    def __init__(self, parameters: dict) -> None:
        super().__init__()
        datasets = parameters['instances']

        if len(datasets) == 0:
            raise Exception("Deve ser definido pelo menos um dataset")
        else:
            self.dataset_factory = GenericFactory(parameters)
            self.insert(0, self.dataset_factory.create)
