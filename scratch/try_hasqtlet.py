import sys
from random import randint

from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
from traitlets import Integer

from qtlets.qtlets import HasQtlets
from qtlets.widgets import IntEdit

class Data(HasQtlets):
    value = Integer(default_value=1, min=0, max=10)


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


def update_cb(change):
    print(f"{change.old} -> {change.new}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = Data(value=3)
    d.observe(update_cb, names="value")
    form = Form(data=d)
    form.show()
    sys.exit(app.exec_())
