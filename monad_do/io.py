from .combinators import *
from .do_cached import do
from .free import Free
from .functor import Functor


class _IOFunctor(Functor):
    def __init__(self, proc):
        self.proc = proc

    def map(self, f):
        return _IOFunctor(compose(f, self.proc))

    def get(self):
        return self.proc()


IO = Free
as_io = compose(IO.lift, _IOFunctor)


def io_input(prompt=None):
    @wraps(input)
    def wrapped():
        return input(prompt)
    return as_io(wrapped)


def io_print(*args, **kwargs):
    @wraps(print)
    def wrapped():
        print(*args, **kwargs)
    return as_io(wrapped)
