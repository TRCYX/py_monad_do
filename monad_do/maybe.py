from .monad import Monad


class Maybe(Monad):
    @staticmethod
    def pure(b):
        return Just(b)

    def bind(self, k):
        raise NotImplementedError

    def is_nothing(self):
        return not self.is_just()

    def is_just(self):
        raise NotImplementedError

    def match(self, n, j):
        raise NotImplementedError

    @staticmethod
    def from_native(a):
        if not isinstance(a, Maybe):
            return Nothing if a is None else Just(a)
        else:
            return a


class NothingType(Maybe):
    def __repr__(self):
        return 'Nothing'

    def bind(self, k):
        return Nothing

    def is_just(self):
        return False

    def match(self, n, j):
        return n


Nothing = NothingType()


class Just(Maybe):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Just({repr(self.value)})'

    def bind(self, k):
        return k(self.value)

    def is_just(self):
        return True

    def match(self, n, j):
        return j(self.value)
