from abc import ABC, abstractmethod
from src.shared.container import Container
from src.shared.generic_factory import GenericFactory


class ItemContainer(Container):
    def __init__(self, parameters: dict = None):
        super().__init__()

        if parameters is not None:
            self.metrics_factory = GenericFactory(parameters)
            self.insert(0, self.metrics_factory.create)


class Item(ABC):
    def __init__(self, parameters: dict = None) -> None:
        self.id = parameters.get('id', None)
        self.create_attributes(parameters)
        self.ratings = []

    def create_attributes(self, attributes: dict):
        for key, value in attributes.items():
            setattr(self, key, value)

class MovieItem(Item):
    def __init__(self, parameters: dict):
        super().__init__(parameters)
        self.genres = parameters.get('genres', None)
        self.title = parameters.get('title', None)
        self.tag = parameters.get('tag', None)
