from .applicative import Applicative
from .combinators import *


class Monad(Applicative):
    def bind(self, k):
        raise NotImplementedError

    def join(self):
        return self.bind(identity)

    def ap1(self, arg):
        return self.bind(lambda a: arg.bind(compose(self.pure, a)))


def mcompose(*k):
    def composed(a):
        return reduce(lambda a, k: a.bind(k), reversed(k), a)
    return composed
