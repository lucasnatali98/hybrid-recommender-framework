from src.shared.container import Container
from src.shared.generic_factory import GenericFactory


class RecommendersContainer(Container):
    def __init__(self, parameters: dict) -> None:
        super().__init__()
        recommenders = parameters.get('instances')

        if len(recommenders) == 0:
            pass
        else:
            self.recommender_factory = GenericFactory(parameters)
            self.insert(0, self.recommender_factory.create)
