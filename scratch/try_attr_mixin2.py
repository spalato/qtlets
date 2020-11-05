import attr

class Mixin(object):  # test mixin please ignore
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.param = []

@attr.s(auto_attribs=True)
class Data1(Mixin):
    value: int = 1

class Data2(Mixin):
    value: int = 1

d1 = Data1()
d2 = Data2()

assert d1.value == d2.value == 1
assert not hasattr(d1, "param")
assert     hasattr(d2, "param")