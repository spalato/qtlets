# qtlets.py
# try to remove boilerplate from QT by using observation behavior

from functools import singledispatch
import logging
from weakref import proxy

from PySide2.QtCore import QObject, Signal, QTimer
from PySide2.QtWidgets import QCheckBox, QLineEdit, QAbstractSpinBox

from .widgets import TypedLineEdit, ValuedComboBox

logger = logging.getLogger(__name__)

# The instance will have a the qtlets in a mapping similar to the traits.
#


class Qtlet(QObject):
    """
    Adapter between `traitlets` notification and Qt Signals and Slots.
    """
    data_changed = Signal(object)  # fallback

    def __init__(self, inst, attr, *a, **kw):
        super().__init__(*a, **kw)
        self.widgets = []  # holds weakref.proxy elements.
        self.inst = inst
        self.attr = attr
        self.timer = None

    @property
    def value(self):
        return getattr(self.inst, self.attr)

    @value.setter
    def value(self, value):
        setattr(self.inst, self.attr, value)

    @property
    def has_widgets(self):
        return len(self.widgets) > 0

    def on_widget_edited(self, value):  # this is a slot
        """
        Update the attribute to given value.
        """
        # note this is exactly the same as @value.setter...
        self.value = value

    def sync_widgets(self):
        """Force the update of all linked widgets with the current value."""
        self.data_changed.emit(self.value)

    def link_widget(self, widget, widget_signal=None, widget_slot=None):
        """Link a widget to the trait."""
        # todo: use a function and dispatch to get the two methods (widget.valueEdited, widget.setValue)
        # todo: add bounds to validator.. here is probably the best, in "link"
        if widget_signal is None:
            widget_signal = notifier_signal(widget)
        widget_signal.connect(self.on_widget_edited)
        if widget_slot is None:
            widget_slot = setter_slot(widget)
        self.data_changed.connect(widget_slot)
        self.widgets.append(proxy(widget))
        self.data_changed.emit(self.value)
        return self

    def use_polling(self, interval: float=20):
        """Checks and update the value on a fixed interval, in ms."""
        if self.timer is None:
            self.timer = QTimer(parent=self)
        self.timer.setInterval(interval)
        self.timer.timeout.connect(self.sync_widgets)
        self.timer.start()
        # TODO: we could need a stop and a teardown...
        return self
        

    # def unlink_widget(self, widget): # this is not used...
    #     notifier_signal(widget).disconnect(widget.setValue)
    #     self.widgets.remove(widget)


class IntQtlet(Qtlet):
    data_changed = Signal(int)


class FloatQtlet(Qtlet):
    data_changed = Signal(float)

class StrQtlet(Qtlet):
    data_changed = Signal(str)


class BoolQtlet(Qtlet):
    data_changed = Signal(bool)

@singledispatch
def qtlet_type(typ):
    logger.debug(f"Could not find specific Qtlet type for: {typ!r}")
    return Qtlet


@qtlet_type.register(int)
def qtl_int(typ):
    return IntQtlet


@qtlet_type.register(float)
def qtl_float(typ):
    return FloatQtlet


@qtlet_type.register(str)
def qtl_str(typ):
    return StrQtlet


@qtlet_type.register(bool)
def qtl_bool(typ):
    return BoolQtlet


@singledispatch
def notifier_signal(widget) -> Signal: # todo: we should probably add another argument
    if hasattr(widget, "valueEdited"):
        return widget.valueEdited
    raise TypeError("Could not find signal for widget")

@notifier_signal.register(QCheckBox)
def notifier_checkbox(widget):
    return widget.clicked

@notifier_signal.register(QAbstractSpinBox)
def notifier_spin(widget):
    return widget.valueChanged

@notifier_signal.register(QLineEdit)
def notifier_linedit(widget):
    return widget.textEdited

@notifier_signal.register(TypedLineEdit)
def notifier_typed(widget):
    return widget.valueEdited


@singledispatch
def setter_slot(widget):
    if hasattr(widget, "setValue"):
        return widget.setValue
    raise TypeError("Could not find setter method for widget")

@setter_slot.register(QCheckBox)
def setter_checkbox(widget):
    return widget.setChecked

@setter_slot.register(QAbstractSpinBox)
def setter_spin(widget):
    return widget.setValue

@setter_slot.register(QLineEdit)
def setter_linedit(widget):
    return widget.setText

@setter_slot.register(TypedLineEdit)
def setter_typed(widget):
    return widget.setValue


class HasQtlets(object):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        # I think defining this here will be ok. We'll create the qtlets later
        self.qtlets = {}


    def link_widget(self, widget, attr_name: str, widget_signal=None,
                    widget_slot=None) -> Qtlet:
        """Link widget to attr"""
        # make sure qlet exists
        if attr_name not in self.qtlets:
            qtl = self.create_qtlet(attr_name)
            self.qtlets[attr_name] = qtl
        else:
            qtl = self.qtlets[attr_name]
        # link qtlet to widget.
        return qtl.link_widget(widget, widget_signal=widget_signal,
                        widget_slot=widget_slot)

    def __setattr__(self, key, value):
        try:
            super().__setattr__(key, value)
        finally:
            if hasattr(self, "qtlets") and key in self.qtlets:
                self.qtlets[key].sync_widgets()

    # def unlink_widget(self, widget, attr_name: str):
    #     # unlink qtlet from widget
    #     # if qtlet doesn't have any widgets left, remove it.
    #     qtl = self.qtlets[attr_name]
    #     qtl.unlink_widget(widget)
    #     if not qtl.has_widgets:
    #         del self.qtlets[attr_name]

    def create_qtlet(self, attr_name: str, cls=None):
        # we need to put this into a function...
        # figure out the correct qtl type
        if cls is None:
            cls = qtlet_type(getattr(self, attr_name))

        qtl = cls(self, attr_name)
        return qtl
