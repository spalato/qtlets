# qtlets.py
# try to remove boilerplate from QT by using taitlets' observation behavior
# what we need is essentially an adapter between traits' observe and Qt signals
# We don't need to change the keys ever, so we'll use instances.

from abc import abstractmethod
from functools import singledispatch

from traitlets import HasTraits, TraitError
import traitlets as trt
from PySide2.QtCore import QObject, Signal

# How do we structure this?
# The instance will be a subclass of the HasQtlet object. We will interact with
# it. The instance will be used for `register_widget`, `sync_widgets`, `movetothread`
#
# The instance will have a the qtlets in a mapping similar to the traits.
#


class Qtlet(QObject):
    """Adapter between `traitlets` notification and Qt Signals and Slots"""
    # define custom signal per type?
    data_changed = Signal(object)  # fallback
    def __init__(self, inst, attr, *a, **kw):
        super().__init__(*a, **kw)
        self.widgets = []
        self.inst = inst # or use this to set attribute of the attribute proxy descriptor?
        self.attr = attr
        inst.observe(self.notify_widgets, names=attr) # link qtlet to traitlet

    # we're building a proxy to act as a descriptor... can we grab the attribute
    # directly?
    @property
    def value(self):
        return getattr(self.inst, self.attr)

    @value.setter
    def value(self, value):
        try:
            setattr(self.inst, self.attr, value)
        except TraitError:  # validation failed
            self.sync_widgets() # resync the widget to current value
            raise

    @property
    def has_widgets(self):
        return len(self.widgets) > 0

    def on_widget_edited(self, value):  # this is a slot
        """
        Update the attribute to given value.
        """
        # note this is exactly the same as @value.setter...
        self.value = value

    def notify_widgets(self, change):
        """
        Update the widgets to reflect a change in the underlying data.
        """
        # todo: find a more elegant way to pick the signal. Maybe it's ok?
        self.data_changed.emit(change.new)

    def sync_widgets(self):
        """Force the update of all linked widgets with the current value."""
        self.data_changed.emit(self.value)

    def link_widget(self, widget): # todo: add options for read and write?
        """Link a widget to the trait."""
        # todo: use a function and dispatch to get the two methods (widget.valueEdited, widget.setValue)
        widget.valueEdited.connect(self.on_widget_edited)
        self.data_changed.connect(widget.setValue)
        self.widgets.append(widget)
        self.data_changed.emit(self.value)

    def unlink_widget(self, widget):
        widget.valueEdited.disconnect(widget.setValue)
        self.widgets.remove(widget)


# todo: add bounds to validator.. here is probably the best, in "link"
class IntQtlet(Qtlet):
    data_changed = Signal(int)

class FloatQtlet(Qtlet):
    data_changed = Signal(float)

@singledispatch
def qtlet_type(trait: trt.TraitType):
    return Qtlet

@qtlet_type.register(trt.Integer)
@qtlet_type.register(trt.CInt)
def qtl_int(trait):
    return IntQtlet

@qtlet_type.register(trt.Float)
@qtlet_type.register(trt.CFloat)
def qtl_float(trait):
    return FloatQtlet


class HasQtlets(HasTraits):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        # I think defining this here will be ok. We'll create the qtlets later
        self.qtlets = {}

    # we may need to intercept the setattr call if there is a qtlet, in order
    # to handle Qt threads...

    def link_widget(self, widget, attr_name: str):
        """Link widget to attr"""
        # make sure qlet exists
        if attr_name not in self.qtlets:
            qtl = self.create_qtlet(attr_name)
            self.qtlets[attr_name] = qtl
        else:
            qtl = self.qtlets[attr_name]
        # link qtlet to widget.
        qtl.link_widget(widget)

    def unlink_widget(self, widget, attr_name: str):
        # unlink qtlet from widget
        # if qtlet doesn't have any widgets left, remove it.
        qtl = self.qtlets[attr_name]
        qtl.unlink_widget(widget)
        if not qtl.has_widgets:
            del self.qtlets[attr_name]

    def create_qtlet(self, attr_name: str):
        # figure out the correct qtl type
        cls = qtlet_type(self.traits()[attr_name])
        # setup
        qtl = cls(self, attr_name)
        return qtl
