import itertools

from .monad import Monad


class List(Monad, list):
    def __repr__(self):
        return f'List({super().__repr__()})'

    @staticmethod
    def pure(a):
        return List([a])

    def bind(self, k):
        return List(list(itertools.chain(*map(k, self))))

    @classmethod
    def from_native(cls, a):
        if isinstance(a, list) and not isinstance(a, List):
            return List(a)
        else:
            return a
