from functools import reduce, wraps


def identity(x):
    return x


def constant(c):
    return lambda x: c


def flip(f):
    @wraps(f)
    def flipped(b):
        def wrapped(a):
            return f(a)(b)
        return wrapped
    return flipped


def compose(*funcs):
    if not funcs:
        return identity

    def composed(*args, **kwargs):
        first_result = funcs[-1](*args, **kwargs)
        return reduce(lambda x, f: f(x), reversed(funcs[:-1]), first_result)

    return composed


def apply(func, *args, **kwargs):
    return func(*args, **kwargs)


def uncurry(func):
    @wraps(func)
    def wrapped(args, kwargs={}):
        return func(*args, **kwargs)
    return wrapped
