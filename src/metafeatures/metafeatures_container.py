from src.metafeatures.factory import *
from src.shared.container import Container


class MetaFeatureContainer(Container):
    def __init__(self, parameters: dict) -> None:
        """

        """
        super().__init__()

        metafeatures = parameters['instances']

        if len(metafeatures) == 0:
            pass
        else:
            self.metafeatures_factory = MetaFeatureFactory(parameters)
            self.insert(0, self.metafeatures_factory.create)

