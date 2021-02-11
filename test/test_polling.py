# test our use of polling

import sys
import time

import pytest

from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QCheckBox, \
    QLineEdit
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest

from qtlets.qtlets import HasQtlets
from qtlets.widgets import IntEdit, StrEdit


@pytest.fixture
def data_instance():
    class Data(HasQtlets):
        def __init__(self, *a, value=0, **kw):
            super().__init__(*a, **kw)
            self._value = value

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, v):
            self._value = v
    return Data()

@pytest.fixture
def form():
    class Form(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.edit = IntEdit(0)
            layout = QVBoxLayout()
            layout.addWidget(self.edit)
    return Form()

@pytest.mark.usefixtures("app")
class TestPolling:
    def test_poll_basic(self, form, data_instance):
        data_instance.link_widget(form.edit, "value").use_polling()
        init_value = 0
        test_value = 13
        data_instance.value = init_value
        assert form.edit.value() == init_value
        data_instance._value = test_value
        assert form.edit.value() == init_value
        data_instance.qtlets["value"].timer.timeout.emit() # good!
        assert form.edit.value() == test_value
