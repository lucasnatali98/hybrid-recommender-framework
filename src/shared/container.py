from typing import TypeVar, Generic, List

T = TypeVar('T')


class Container(Generic[T]):
    """
    A classe Container tem como objetivo generalizar para diversos tipos as operações
    de push, insert, remove, clear, etc
    """
    instance_type: object

    def __init__(self, instance_type=None) -> None:
        """
        A classe Container tem o objetivo de generalizar o armazenamento de items de um tipo T

        """
        self.instance_type = instance_type
        self.items: List[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

    def insert(self, index, items: List[T]) -> None:
        self.items.insert(index, items)

    def remove(self, item: T) -> None:
        self.items.remove(item)

    def remove_all(self):
        self.items.clear()

    def print_instances(self):
        for i in self.items:
            print(i)

    def is_structure_empty(self, structure: List[T]) -> bool:
        if len(structure) == 0:
            return True

        return False

    def find(self, elem):
        new_elem = list(filter(lambda x: x == elem, self.items))
        if len(new_elem) == 0:
            return None

        return new_elem[0]

    def get_items(self):
        return self.items
