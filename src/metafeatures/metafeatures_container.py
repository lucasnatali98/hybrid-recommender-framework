from src.metafeatures.factory import *
from src.shared.container import Container


class MetaFeatureContainer(Container):
    def __init__(self, parameters: dict) -> None:
        """

        """
        super().__init__()

        metafeatures = parameters['instances']

        if len(metafeatures) == 0:
            self.metafeatures_objects = []
        else:
            self.metafeatures_objects = []
            self.metafeatures_factory = MetaFeatureFactory(parameters)
            self.metafeatures_objects = self.metafeatures_factory.create

