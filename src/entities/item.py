from abc import ABC, abstractmethod
from src.shared.container import Container
from src.shared.generic_factory import GenericFactory

class ItemContainer(Container):
    def __init__(self, parameters: dict):
        super().__init__()
        self.metrics_factory = GenericFactory(parameters)
        self.insert(0, self.metrics_factory.create)



class Item(ABC):
    def __init__(self, parameters: dict) -> None:
        self.id = parameters.get('id', None)
        self.ratings = []


class MovieItem(Item):
    def __init__(self, parameters: dict):
        super().__init__(parameters)
        self.genres = parameters.get('genres', None)
        self.title = parameters.get('title', None)
        self.tag = parameters.get('tag', None)





