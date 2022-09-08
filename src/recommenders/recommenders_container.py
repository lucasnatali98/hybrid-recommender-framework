from src.recommenders.factory import *
from src.shared.container import Container

class RecommendersContainer(Container):
    """

    """

    def __init__(self, parameters: dict):
        """
        @type stages: list

        """

        super().__init__()
        recommenders = parameters['recommenders']

        if len(recommenders) == 0:
            self.recommenders_object = []
        else:
            self.recommenders_object = []
            self.recommender_factory = RecommenderFactory(parameters)
            self.recommenders_object = self.recommender_factory.create
