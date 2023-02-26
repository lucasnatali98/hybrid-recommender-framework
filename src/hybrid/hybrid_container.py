from src.shared.container import Container
from src.shared.generic_factory import GenericFactory


class HybridContainer(Container):
    def __init__(self, parameters: dict) -> None:
        super().__init__()
        stages = parameters.get('instances')

        if len(stages) == 0:
            pass
        else:
            self.hybrid_factory = GenericFactory(parameters)
            self.insert(0, self.hybrid_factory.create)
