from .monad import Monad


class State(Monad):
    def __init__(self, f):
        self.f = f

    @staticmethod
    def pure(a):
        return State(lambda s: (a, s))

    def bind(self, k):
        def f(s):
            a, s_ = self.f(s)
            return k(a)(s_)
        return State(f)

    def run(self, s):
        return self.f(s)

    def __call__(self, s):
        return self.f(s)

    def eval(self, s):
        return self.f(s)[0]

    def exec(self, s):
        return self.f(s)[1]

    @staticmethod
    def from_native(f):
        if not isinstance(f, State) and callable(f):
            return State(f)
        else:
            return f


get = State(lambda s: (s, s))


def gets(f):
    return State(lambda s: (f(s), s))


def put(s):
    return State(lambda _: ((), s))


def modify(f):
    return State(lambda s: ((), f(s)))
