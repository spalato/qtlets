# test the ability to supply custom signal and slots
from random import randint, choices
from string import ascii_letters, punctuation, digits

import pytest

from PySide2.QtWidgets import QWidget, QLineEdit, QDoubleSpinBox, QVBoxLayout

from qtlets import HasQtlets

printable = ascii_letters + punctuation + digits

# matrix:
# Try qlineedit, qspinbox
# try explicit, auto


@pytest.fixture
def data_instance():
    class Data(HasQtlets):
        def __init__(self, *args, text="test", number=1, **kwargs):
            super().__init__(*args, **kwargs)
            self.text = text
            self.number = number
    return Data()

@pytest.fixture(
    params = (
        [("textEdited", "setText"), ("valueChanged", "setValue")],
        [(None, None), (None, None)],
             ),
    ids = ["explicit",
           "auto",
           ]
)
def sig_names(request):
    return request.param


@pytest.fixture
def form(sig_names, data_instance):
    (tsig, tslt), (nsig, nslt) = sig_names
    # I'm testing two things together...
    class Form(QWidget):
        def __init__(self, data=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.data = data

            self.lineedit = QLineEdit("")
            self.spin = QDoubleSpinBox()

            self.setLayout(QVBoxLayout())
            for w in [self.lineedit, self.spin]:
                self.layout().addWidget(w)

            data.link_widget(
                self.lineedit, "text",
                widget_signal=tsig and getattr(self.lineedit, tsig),
                widget_slot=tslt and getattr(self.lineedit, tslt),
            )
            data.link_widget(
                self.spin, "number",
                widget_signal=nsig and getattr(self.spin, nsig),
                widget_slot=nslt and getattr(self.spin, nslt),
            )

        def new_values(self):
            while (target := randint(0,10)) == self.data.number:
                pass
            self.data.number = target
            while (target := "".join(choices(printable, k=10))) == self.data.text:
                pass
            self.data.text = target

    return Form(data=data_instance)

@pytest.mark.usefixtures("app")
class Test_named_signals:
    def test_initial_sync(self, data_instance, form):
        assert data_instance.text == form.lineedit.text()
        assert data_instance.number == form.spin.value()

    @pytest.mark.usefixtures("app")
    def test_external(self, data_instance, form):
        form.new_values()
        assert data_instance.text == form.lineedit.text()
        assert data_instance.number == form.spin.value()

