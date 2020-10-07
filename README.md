# qtlets
Automatic linking of data to qt widgets. MCV without the boilerplate.

`qtlets` aims at providing a simple way to keep in sync widgets and data. We 
wish to perform this without forcing users of the library to redesign and
rewrite their classes in any way. Currently, bidirectional linking can be
performed in a single call:
`my_instance.link(my_widget, attribute_name)`

This library is currently in early stages. The desired  behavior is achieved 
using a mixin class, `HasQtlets`. Some basic scalar data types are supported. 
The target widgets must currently be made 'type-aware', ie: capable of 
receiving and sending the correct data type. 

# Getting started

Create an environment with python 3.8

## Install dependencies
```
pip install -r requirements.txt
pip install -e .
```

## Run tests
`python -m unittest`

# Plan

We aim to achieve (in rough priority order):
- Keep in sync widgets and data, cutting on the boilerplate.
  eg: `my_instance.link(my_widget, attribute_name)` 
- No need to design our classes and objects with Qt in mind. The rule is that
  if your class works well, and you want to keep it, you can. We should dress
  it up as lightly as possible.
- Compatibility with anything: both simple builtins (naked classes) and complex
  third-party classes (ex: traitlets).
- Support properties
- Support for collections attributes (ex: `instance.values = []`)
- Support for mutable types (dict, list, etc.)
- Support polling (`inst.link(widget, attrname, poll_interval=15)`)
- Leverage Qt's thread affinity when using signals and slots, for setting as 
  well as for getting. 
- Streamlined type conversions and checks
- Dedicated widgets.
- Use either PySide2 or PyQt. See how pyqtgraph does it.
