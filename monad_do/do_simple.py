from functools import wraps

from .combinators import *
from .cont import *
from .either import *


class _Continuation:
    def __init__(self, generator_creator, history=[None]):
        self.generator_creator = generator_creator
        self.history = history

    def send(self, b):
        return _Continuation(self.generator_creator, self.history + [b])

    def get(self):
        g = self.generator_creator()
        try:
            for h in self.history:
                a = g.send(h)
            return Left(a)
        except StopIteration as exc:
            return Right(exc.value)


def _transform(_cont):
    e = _cont.get()

    def if_left(cont_b):
        def transformed(b):
            return _transform(_cont.send(b))
        return cont_b.bind(transformed)

    return e.match(if_left, identity)


def _do_impl_cont(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return _transform(_Continuation(lambda: f(*args, **kwargs)))
    return wrapped


def _to_cont(f, m):
    @wraps(f)
    def wrapped(*args, **kwargs):
        g = f(*args, **kwargs)
        a = None
        try:
            while True:
                a = yield Cont(m.from_native(g.send(a)).bind)
        except StopIteration as exc:
            return Cont.pure(m.from_native(exc.value))
    return wrapped


def do(m):
    if m is Cont:
        return _do_impl_cont
    else:
        return lambda f: compose(lambda c: c.run(identity), _do_impl_cont(_to_cont(f, m)))
