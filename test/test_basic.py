import sys
from random import randint
import unittest

from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
from traitlets import Integer

from qtlets.qtlets import HasQtlets
from qtlets.widgets import IntEdit

app = QApplication(sys.argv)

class TestBasic(unittest.TestCase):
    def setUp(self):
        class Data(HasQtlets):
            value = Integer(default_value=1, min=0, max=10)

        class Form(QWidget):
            def __init__(self, parent=None, data=None):
                super().__init__(parent)
                self.data = data

                self.edit = IntEdit("...")
                self.otheredit = IntEdit("???")
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
                print("Roll!!")
                # this is done in the calling thread.
                # We're not exploiting Qt's queued events in this direction
                self.data.value = randint(0, 10)

        d = Data(value=3)
        form = Form(data=d)
        self.form = form
        self.data = d


    def test_external(self):
        self.data.value += 1
        self.assertEqual(self.data.value, self.form.edit.value())
        self.assertEqual(self.data.value, self.form.otheredit.value())


if __name__ == '__main__':
    unittest.main()
    