from functools import wraps

from fastcache import clru_cache

from .combinators import *
from .cont import *
from .either import *


class _Continuation:
    def __init__(self, generator_creator, history=[], value_to_feed=None, saved_generator=None):
        self.generator_creator = generator_creator
        self.history = history
        self.saved_generator = saved_generator
        self.value_to_feed = value_to_feed
        self.value_produced = None

        @clru_cache(typed=True, unhashable='ignore')
        def send(b):
            assert not isinstance(self.value_produced, Right)
            new_history = self.history + [self.value_to_feed]

            if self.saved_generator is None:
                return _Continuation(self.generator_creator, new_history, b)

            if self.value_produced is None:
                self._feed()
            ret = _Continuation(self.generator_creator,
                                new_history, b, self.saved_generator)
            self._clear()
            return ret

        self.send = send

    def _create_generator(self):
        g = self.generator_creator()
        for h in self.history:
            g.send(h)
        self.saved_generator = g

    def _feed(self):
        try:
            a = self.saved_generator.send(self.value_to_feed)
        except StopIteration as exc:
            self.value_produced = Right(exc.value)
        else:
            self.value_produced = Left(a)

    def _clear(self):
        self.saved_generator = None

    def get(self):
        if self.value_produced is None:
            if self.saved_generator is None:
                self._create_generator()
            self._feed()

        return self.value_produced


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
