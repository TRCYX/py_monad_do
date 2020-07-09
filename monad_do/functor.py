class Functor:
    def map(self, f):
        raise NotImplementedError

    @staticmethod
    def from_native(a):
        return a
