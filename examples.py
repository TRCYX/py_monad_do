from monad_do import *

# from monad_do.do_simple import do


def fdiv(a, b):
    if b == 0:
        return Left(f'{a} cannot be divided by 0')
    else:
        return Right(a / b)


@do(Either)
def test_either(a, b):
    print('run once')
    val1 = yield fdiv(2.0, a)
    val2 = yield fdiv(b, 1.0)
    val3 = yield fdiv(val1, val2)
    return val3


print(test_either(2, 4))
print(test_either(0, 4))
print(test_either(2, 0))
print(test_either(0, 0))


@do(List)
def test_list(a, b):
    x = yield [a * 10, a]
    y = yield [b * 100, b * 10, b]
    return [x + y]


print(test_list(3, 4))


def push(x):
    return modify(lambda l: l + [x])


pop = modify(lambda l: l[:-1])


@do(State)
def test_state(x):
    not_empty = gets(bool)
    last = gets(lambda l: l[-1])
    while (yield not_empty) and (yield last) < x:
        yield pop
    yield push(x)
    return State.pure(())


print(test_state(5).run([6, 7, 3, 1]))
print(test_state(5).run([4, 3, 1]))


def test_cont(n):
    def iter(n, p):
        @do(Cont)
        def body(return_):
            if n <= 1:
                yield return_(p)
            else:
                yield iter(n - 1, p * n)(return_)
            raise RuntimeError("Never reached")
        return body
    return callcc(iter(n, 1))


print(test_cont(10).run(identity))


@do(IO)
def echo():
    @do(IO)
    def loop():
        s = yield io_input('echo> ')
        if s != 'exit':
            yield io_print(s)
            return loop()
        else:
            return IO.pure(())

    yield io_print('-- The echo program --')
    yield io_print('Type "exit" to exit')
    return loop()

e = echo()
e.run()
