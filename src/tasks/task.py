from abc import ABC, abstractmethod


class Task(ABC):

    @abstractmethod
    def check_args(self, args):

        """

        @param args:
        @return:
        """
        pass

    @abstractmethod
    def run(self):
        """

        @return:
        """
        pass

