from src.shared.container import Container
from src.shared.generic_factory import GenericFactory


class MetaFeatureContainer(Container):
    def __init__(self, parameters: dict) -> None:
        """

        """
        super().__init__()

        metafeatures = parameters.get('instances')

        if len(metafeatures) == 0:
            pass
        else:
            self.metafeatures_factory = GenericFactory(parameters)
            self.insert(0, self.metafeatures_factory.create)

