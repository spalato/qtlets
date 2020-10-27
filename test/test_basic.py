import sys
from collections import namedtuple
from functools import partial
from random import randint, choices
from string import ascii_letters, punctuation, digits
from types import SimpleNamespace

import pytest


from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest

from qtlets.qtlets import HasQtlets
from qtlets.widgets import IntEdit, StrEdit

TRAITLETS_IS_AVAILABLE = False
try:
    from traitlets import Integer, HasTraits, Unicode
    TRAITLETS_IS_AVAILABLE = True
except ImportError:
    pass
ATTR_IS_AVAILABLE = False
try:
    import attr  # attr is a dependency of pytest...
    ATTR_IS_AVAILABLE = True
except ImportError:
    pass

printable = ascii_letters + punctuation + digits

@pytest.fixture(scope="session")
def app():
#    if (app := QApplication.instance()) is None:
    app = QApplication([])
    return app

@pytest.fixture(params=[int, str])
def data_type(request):
    return request.param

dtypes = {
    str: SimpleNamespace(
        dtype=str,
        init_value="TEST",
        random_value=lambda : "".join(choices(printable, k=10)),
        edit_type=StrEdit),
    int: SimpleNamespace(
        dtype=int,
        init_value=1,
        random_value=lambda : randint(0, 10),
        edit_type=IntEdit)
}
if TRAITLETS_IS_AVAILABLE:
    dtypes[str].traitlet = Unicode
    dtypes[int].traitlet = Integer

@pytest.fixture
def dtype_config(data_type):
    return dtypes[data_type]


def vanilla(dtype_config):
    v = dtype_config.init_value
    class Data(HasQtlets):
        def __init__(self, *a,
                     value=v,
                     **kw):
            super().__init__(*a, **kw)
            self.value = value
    return Data()

def traitlets(dtype_config):
    class Data(HasQtlets, HasTraits):
        value = dtype_config.traitlet(default_value=dtype_config.init_value)
    return Data()

def attrs(dtype_config):
    @attr.s
    class Data(HasQtlets):
        value: dtype_config.dtype = attr.ib(default=dtype_config.init_value)
        def __attrs_post_init__(self):
            super().__init__() # tsk tsk tsk...
    return Data()


@pytest.fixture(
    params=[
        vanilla,
        pytest.param(traitlets,
            marks=pytest.mark.skipif(not TRAITLETS_IS_AVAILABLE, reason="Requires the `traitlets` module.")
        ),
        pytest.param(attrs,
            marks=pytest.mark.skipif(not ATTR_IS_AVAILABLE, reason="Requires the `attrs` module.")
        ),
    ]
)
def data_instance(request, dtype_config):
    return request.param(dtype_config)


@pytest.fixture
def new_value(dtype_config):
    def f(current):
        while (target := dtype_config.random_value()) == current:
            pass
        return target
    return f

@pytest.fixture
def form(dtype_config, data_instance, new_value):
    edit_cls = dtype_config.edit_type
    class Form(QWidget):
        def __init__(self, parent=None, data=None):
            super().__init__(parent)
            self.data = data
            self.edit = edit_cls("...")

            self.otheredit = edit_cls("???")
            # self.otheredit.setEnabled(False)
            self.button = QPushButton("Roll!")

            layout = QVBoxLayout()
            for w in [self.edit, self.otheredit, self.button]:
                layout.addWidget(w)
            self.setLayout(layout)

            data.link_widget(self.edit, "value")
            data.link_widget(self.otheredit, "value")

            self.button.clicked.connect(self.on_btn_click)
            self.setWindowTitle("Directional connection")

        def on_btn_click(self):
            self.data.value = new_value(self.data.value)

    return Form(data=data_instance)


@pytest.mark.usefixtures("app")
class TestBasic:

    def test_initial_sync(self, data_instance, form):
        assert data_instance.value == form.edit.value()
        assert data_instance.value == form.otheredit.value()

    def test_external(self, data_instance, form, new_value):
        data_instance.value = new_value(data_instance.value)
        assert data_instance.value == form.edit.value()
        assert data_instance.value == form.otheredit.value()

    def test_roll(self, data_instance, form):
        old = data_instance.value
        #while data_instance.value == old:
        QTest.mouseClick(form.button, Qt.LeftButton)
        assert old != data_instance.value
        assert data_instance.value == form.edit.value()
        assert data_instance.value == form.otheredit.value()

    def test_modify_edit(self, data_instance, form, new_value):
        target = new_value(data_instance.value)
        assert target != data_instance.value
        for w in (form.edit, form.otheredit):
            w.clear()
            QTest.keyClicks(w, str(target))
            QTest.keyClick(w, Qt.Key_Enter)
            assert data_instance.value == form.edit.value()
            assert data_instance.value == form.otheredit.value()
            assert data_instance.value == target

