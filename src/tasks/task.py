from abc import ABC, abstractmethod


class Task(ABC):

    @abstractmethod
    def check_args(self, args):
        pass

    @abstractmethod
    def run(self):
        pass
