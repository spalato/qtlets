import logging

from PySide2.QtCore import Signal
from PySide2.QtGui import QIntValidator, QDoubleValidator
from PySide2.QtWidgets import QPushButton, QLabel, QComboBox, QLineEdit


class TypedLineEdit(QLineEdit):
    def __init__(self, contents, *a, **kw):
        super().__init__(str(contents), *a, **kw)
        self.editingFinished.connect(self.onValueEdited)

    def onValueEdited(self):
        self.valueEdited.emit(self.value())

    def setValue(self, v):
        self.setText(str(v))


class IntEdit(TypedLineEdit):
    valueEdited = Signal(int)

    def __init__(self, *a,
                 bottom: int = None, top: int = None,
                 **kw):
        """
        Line edit for integer.

        Automates type conversion and includes a Validator. Parameters `minimum`
        and `maximum` are used to setup the validator. All other parameters are
        forwarded to QLineEdit.

        Parameters:
        -----------
        minimum : int
            Set minimum value for validator.
        maximum : int
            Set maximum value for validator.

        """
        super().__init__(*a, **kw)
        self.setValidator(QIntValidator())
        if bottom is not None: self.validator().setBottom(bottom)
        if top is not None: self.validator().setTop(top)

    def value(self):
        return int(self.text())


class FloatEdit(TypedLineEdit):
    valueEdited = Signal(float)

    def __init__(self, *a,
                 bottom: float = None, top: float = None, decimals: int = None,
                 **kw):
        """
        Line edit for float.

        Automates type conversion and includes a Validator. Parameters `bottom`,
        `top` and `decimals` are used to setup the validator. All other
        parameters are forwarded to QLineEdit.

        """
        super().__init__(*a, **kw)
        self.setValidator(QDoubleValidator())
        if bottom is not None: self.validator().setBottom(bottom)
        if top is not None: self.validator().setTop(top)
        if decimals is not None: self.validator().setDecimals(decimals)

    def value(self):
        return float(self.text())


class StrEdit(TypedLineEdit):
    valueEdited = Signal(str)

    def value(self):
        return self.text()