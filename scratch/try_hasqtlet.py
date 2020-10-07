import sys
from random import randint

from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication

from qtlets.qtlets import HasQtlets
from qtlets.widgets import IntEdit

class Data(HasQtlets):
    def __init__(self, value=1, *a, **kw):
        super().__init__(*a, **kw)
        self.value = value


class Form(QWidget):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = data

        self.edit = IntEdit("...")
        self.otheredit = IntEdit("???")
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
        self.data.value = randint(0, 10)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = Data(value=3)
    form = Form(data=d)
    form.show()
    sys.exit(app.exec_())
