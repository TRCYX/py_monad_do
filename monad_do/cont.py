from .combinators import *
from .monad import Monad


class Cont(Monad):
    def __init__(self, c):
        self.c = c

    def __repr__(self):
        return f'Cont({repr(self.c)})'

    @staticmethod
    def pure(a):
        return Cont(lambda f: f(a))

    def bind(self, k):
        return Cont(lambda b2r: self.c(flip(lambda a: k(a).c)(b2r)))

    def run(self, f):
        return self.c(f)

    def __call__(self, f):
        return self.c(f)

    @staticmethod
    def from_native(f):
        if not isinstance(f, Cont) and callable(f):
            return Cont(f)
        else:
            return f


def callcc(f):
    def cont(k):
        def ret(a):
            return Cont(lambda _: k(a))
        return f(ret).run(k)
    return Cont(cont)
