# py_monad_do

A simple monad do notation implementation with nice syntax using generators. Also includes sample monads such as `Maybe` and `List`.

Sample code:

```python
from monad_do import *

@do(List)
def test_list(a, b):
    x = yield [a * 10, a] # Native lists are coerced into monad Lists here.
    y = yield [b * 100, b * 10, b]
    return [x + y]


print(test_list(3, 4)) # List([430, 70, 34, 403, 43, 7])
```

Monad instances derive from the `Monad` class and provide the methods `pure`(static) and `bind`. The `do` decorators binds the values yielded from a generator to its later computation. In a sense, `yield` works like `<-` in Haskell.

Note that generators are uncopyable, so if some code needs to be run more than once (such as the case for the `List` monad), the generator is run from the beginning once again, with the values sent into it recorded to eliminate duplicate computation. This requires that the generators decorated by `do` to be more or less "pure".

The `do` decorator is implemented inside `monad_do.do_cached`. There is also a simpler implementation in `monad_do.do_simple` which sketches the basic idea, but runs the generator from the beginning for each `yield`.

The implementation is primarily inspired by these following materials:
- [Monads and Do-Blocks in Python](https://blog.bede.io/do-notation-for-monads-in-python/) implements a do notation for the `List` monad through recording sent values.
- [Monads in Python (with nice syntax!)](http://www.valuedlessons.com/2008/01/monads-in-python-with-nice-syntax.html) also implements a similar do notation which universally handle monads that only run the generator once.
- [The Mother of all Monads](https://www.schoolofhaskell.com/school/to-infinity-and-beyond/pick-of-the-week/the-mother-of-all-monads) gives the idea of implementing other monads through the `Cont` monad.

Type hints are not incorporated. For now, the weak support for function types (on arguments) makes type hinting more of a burden then something helpful.

### Acknowledgements

Thank @danoneata for adding the `Reader` Monad.
