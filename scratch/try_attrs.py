import attr


class MyMixin(object):
    def __init__(self, *a, param=True, **kw):
        print(f"MyMixin.__init__ of {type(self)})")
        self.param = param
        super().__init__(*a, **kw)

@attr.s
class A:
    value: int = attr.ib(default=3)

class B(A, MyMixin):
    pass

class C(MyMixin, A):
    pass

@attr.s
class Aprime:
    value: int = attr.ib(default=3)

Aprime = type("Aprime", (MyMixin, Aprime), {})

@attr.s
class Adouble(MyMixin):
    value: int = attr.ib(default=3)

    def __attrs_post_init__(self):
        super().__init__()  # hum...


a = A()
b = B()
c = C()
ap = Aprime()
ad = Adouble()

assert a.value == 3
assert b.value == 3
assert c.value == 3
assert ap.value == 3
assert ad.value == 3

