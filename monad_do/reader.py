from .monad import Monad
from .combinators import identity, constant


class Reader(Monad):
    def __init__(self, f):
        self.f = f

    @staticmethod
    def pure(a):
        return Reader(constant(a))

    def bind(self, g):
        def f(e):
            a = self.f(e)
            return g(a)(e)
        return Reader(f)

    def run(self, e):
        return self.f(e)

    def __call__(self, e):
        return self.f(e)

    @staticmethod
    def from_native(f):
        if not isinstance(f, Reader) and callable(f):
            return Reader(f)
        else:
            return f


ask = Reader(identity)


def local(f, reader):
    return Reader(lambda e: reader.run(f(e)))
