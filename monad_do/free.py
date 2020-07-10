from .monad import Monad


class Free(Monad):
    @staticmethod
    def pure(a):
        return Pure(a)

    @staticmethod
    def lift(a):
        return Roll(a.map(Pure))

    def fold(self, phi):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        return self.fold(lambda f: f.get(*args, **kwargs))


class Pure(Free):
    def __init__(self, value):
        self.value = value

    def bind(self, k):
        return k(self.value)

    def fold(self, phi):
        return self.value


class Roll(Free):
    def __init__(self, value):
        self.value = value

    def bind(self, k):
        return Roll(self.value.map(lambda x: x.bind(k)))

    def fold(self, phi):
        return phi(self.value.map(lambda x: x.fold(phi)))
