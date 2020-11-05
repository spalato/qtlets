# test copying of HasQtlets instances.
# we want to make sure that copying an instance will *not* sync the instance
# and widget.

from copy import copy, deepcopy
from random import randint

import pytest
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest
from PySide2.QtWidgets import QWidget, QVBoxLayout
from qtlets import HasQtlets
from qtlets.widgets import IntEdit


@pytest.fixture
def form():
    class Form(QWidget):
        def __init__(self, parent=None, data=None):
            super().__init__(parent)
            self.data = data
            self.edit = IntEdit(0)

            self.setLayout(QVBoxLayout())
            self.layout().addWidget(self.edit)
    return Form()


@pytest.fixture
def data():
    class Data(HasQtlets):
        def __init__(self, *a, value=3, **kw):
            super().__init__(*a, **kw)
            self.value = value
    return Data()


def new_value(current):
    while (new := randint(0, 10)) == current:
        pass
    return new

@pytest.mark.usefixtures("app")
@pytest.mark.parametrize("copyfunc", [copy, deepcopy])
def test_copy_instance(form, data, copyfunc):
    if copyfunc is deepcopy:
        pytest.xfail("Deepcopy of Qtlets is not possible (they inherit from QObject)")
    # TODO this will need to be extended when we add mutable attributes (collections)
    data.link_widget(form.edit, "value")

    old_value = data.value
    new_data = copyfunc(data)
    target = new_value(old_value)
    assert target != old_value

    # enter a new value
    w = form.edit
    w.clear()
    QTest.keyClicks(w, str(target))
    QTest.keyClick(w, Qt.Key_Enter)

    assert data.value == w.value()  # we kept the first one in sync
    assert new_data.value != w.value()  # our copied object didn't get updated.
