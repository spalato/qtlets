# qtlets
Automatic linking of data to qt widgets. MCV without the boilerplate.

`qtlets` provides a simple way to keep in sync Qt widgets and data, without 
forcing a redesign of your data classes. The rule is: *if you like your class, you can
keep your class*. 

Currently, bidirectional linking can be performed in a simple call<sup>1</sup>:
`instance.link_widget(my_widget, "name")`
The data displayed on `my_widget` will be updated whenever `instance.name` is
modified. Changing the value on `my_widget` will update `instance.name`. 
Multiple widgets can be kept synchronized in this way.
 
This functionnality is provided by a lightweight Mixin class called `HasQtlets`.
To enable `qtlets` on an `Existing` class, simply do:
```
class Data(HasQtlets, Existing): pass
``` 
and then use `Data` as a drop-in replacement for `Existing`.

This library is currently in early stages. The documentation is light, and 
the API is changing quickly. All help is appreciated...

<sup>1</sup> Some conditions currently apply, see the Features section.

# Getting started

Requires an environment with python 3.8.

## Install dependencies
```
pip install -r requirements.txt
pip install -e .
```

## Run tests
`py.test`

# Features

The following features are currently supported:
- Linking of widgets and data. Currently, scalar data members are supported;
- Multiple widgets can be linked with the same data attribute;
- Compatibility with simple vanilla classes, as well as more complex 
  third-party libraries such as `traitlets` (Even `attrs`! Isn't inheritance 
  wonderful?);
- Support for `properties`;
- The signal and slots used to communicate with the widget can be specified
  explicitely. For some widgets, a reasonable default is provided. 


The following features are desired:
- Adding more data types and widgets.
- Streamlined type conversions and checks.
- Support for collections attributes (ex: `instance.values = []`)
- Support polling (`inst.link(widget, attrname, poll_interval=15)`)
- Leverage Qt's thread affinity when using signals and slots, for setting as 
  well as for getting. 
- More dedicated widgets.
- Use either PySide2 or PyQt. See how pyqtgraph does it.
