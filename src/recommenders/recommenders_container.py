from src.shared.container import Container
from src.shared.generic_factory import GenericFactory


class RecommendersContainer(Container):
    def __init__(self, parameters: dict) -> None:
        super().__init__()
        recommenders = parameters.get('instances')
        self.number_of_recommendations = parameters.get('number_of_recommendations')

        if len(recommenders) == 0:
            pass
        else:
            self.recommender_factory = GenericFactory(parameters)
            self.insert(0, self.recommender_factory.create)

    def _apply_number_of_recs_to_recommenders(self):
        pass
