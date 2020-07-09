from .monad import Monad


class Either(Monad):
    @staticmethod
    def pure(b):
        return Right(b)

    def bind(self, k):
        raise NotImplementedError

    def is_left(self):
        return not self.is_right()

    def is_right(self):
        raise NotImplementedError

    def match(self, l, r):
        raise NotImplementedError

    @staticmethod
    def from_native(a):
        if not isinstance(a, Either):
            return Left(None) if a is None else Right(a)
        else:
            return a


class Left(Either):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Left({repr(self.value)})'

    def bind(self, k):
        return Left(self.value)

    def is_right(self):
        return False

    def match(self, l, r):
        return l(self.value)


class Right(Either):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Right({repr(self.value)})'

    def bind(self, k):
        return k(self.value)

    def is_right(self):
        return True

    def match(self, l, r):
        return r(self.value)
