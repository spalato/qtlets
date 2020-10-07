import sys
from random import randint
import unittest

from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest

from qtlets.qtlets import HasQtlets
from qtlets.widgets import IntEdit


class TestBasic(unittest.TestCase):

    def make_data(self):
        class Data(HasQtlets):
            def __init__(self, *a,
                         value=1,
                         **kw):
                super().__init__(*a, **kw)
                self.value = value
        return Data(value=3)

    def make_form(self, *a, **kw):
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
                self.data.value = randint(0, 10)
        return Form(*a, **kw)


    def setUp(self):
        if (app := QApplication.instance()) is None:
            app = QApplication([])
        self.app = app
        self.data = self.make_data()
        self.form = self.make_form(data=self.data)

    def test_external(self):
        self.data.value += 1
        self.assertEqual(self.data.value, self.form.edit.value())
        self.assertEqual(self.data.value, self.form.otheredit.value())

    def test_roll(self):
        old = self.data.value
        while self.data.value == old:
            QTest.mouseClick(self.form.button, Qt.LeftButton)
        self.assertNotEqual(old, self.data.value)
        self.assertEqual(self.data.value, self.form.edit.value())
        self.assertEqual(self.data.value, self.form.otheredit.value())

    def test_modify_edit(self):
        while (target := randint(0, 10)) == self.data.value:
            pass
        self.assertNotEqual(target, self.data.value)
        for w in (self.form.edit, self.form.otheredit):
            w.clear()
            QTest.keyClicks(w, str(target))
            QTest.keyClick(w, Qt.Key_Enter)
            self.assertEqual(target, self.form.edit.value())
            self.assertEqual(target, self.form.otheredit.value())
            self.assertEqual(target, self.data.value)



if __name__ == '__main__':
    unittest.main()
