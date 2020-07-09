from functools import partial, reduce

from .combinators import *
from .functor import Functor


class Applicative(Functor):
    @staticmethod
    def pure(a):
        raise NotImplementedError

    def ap1(self, arg):
        raise NotImplementedError

    def product(self, other):
        return self.map(partial(partial, lambda a, b: (a, b))).ap1(other)

    def ap(self, *args, **kwargs):
        f1 = self.map(partial(partial, lambda f, args: partial(f, *args)))
        args_combined = reduce(lambda l, a: l.product(a).map(
            lambda t: t[0] + [t[1]]), args, self.pure([]))
        f2 = f1.ap1(args_combined).map(partial(partial, lambda f, kwargs: f(**kwargs)))
        kwargs_combined = reduce(lambda d, a: d.product(a[1]).map(
            lambda t: {**t[0], a[0]: t[1]}), kwargs.items(), self.pure({}))
        return f2.ap1(kwargs_combined)

    def map(self, f):
        return self.pure(f).ap1(self)


def liftA(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if args:
            representative = args[0]
        elif kwargs:
            representative = next(iter(kwargs.values()))
        else:
            raise NotImplementedError("No Applicative specified")
        return representative.pure(func).ap(*args, **kwargs)
    return wrapped
