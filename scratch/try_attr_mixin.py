import attr


class Mixin(object):  # test mixin please ignore
    def __init__(self, *args, **kwargs):
        self.param = []
        super().__init__(*args, **kwargs)


# Inheritance case 1
@attr.s
class Data1(Mixin, object):
    value: int = attr.ib(default=1)


# Inheritance case 2
@attr.s
class Base2(object):
    value: int = attr.ib(default=1)


class Data2(Mixin, Base2): pass


# make instances
d1 = Data1()
d2 = Data2()

assert hasattr(d1, "value")
assert hasattr(d2, "value")

assert isinstance(d1, Mixin)
assert isinstance(d2, Mixin)

# SHOCKING

assert not hasattr(d1, "param")
assert     hasattr(d2, "param")  # extra whitespace for emphasis

