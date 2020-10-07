import sys
from random import choices
from string import printable

from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication

from qtlets.qtlets import HasQtlets
from qtlets.widgets import StrEdit



class Data(HasQtlets):
    def __init__(self, value="test", *a, **kw):
        super().__init__(*a, **kw)
        self.value = value


class Form(QWidget):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = data

        self.edit = StrEdit("...")
        self.otheredit = StrEdit("???")
        #self.otheredit.setEnabled(False)
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
        self.data.value = "".join(choices(printable, k=10))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = Data(value="_1")
    form = Form(data=d)
    form.show()
    sys.exit(app.exec_())
