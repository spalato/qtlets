# qtlets
Automatic linking of data to qt widgets. MCV without the boilerplate.

Desires (in rough priority order):
- Keep in sync widgets and data, cutting on the boilerplate.
  eg: `link(widget, instance, attr_name)`, `widget.link(instance, attr_name)`,
  `instance.link(widget, attr_name)` (currently we have the last one).
- No need to design our classes and objects with Qt in mind. The rule is that
  if your class works well, and you want to keep it, you can. We should dress
  it up as lightly as possible.
- Compatibility with anything: both simple builtins (naked classes) and complex
  third-party classes (ex: traitlets). Maybe mutables (ex: specific dict keys.)
- Leverage Qt's thread affinity when using signals and slots, for setting also. 
- Streamlined type conversions and checks
- Dedicated widgets.
- Use either PySide2 or PyQt. See how pyqtgraph does it.

Roadmap:
[x] Finish migrating (not done!)
[x] Convert current `scratch/try_hasqtlet` to a basic smoke test.
[ ] Refactor.

# Design

There are multiple ways to go about this. We want to provide behavior and ease
of use. There will likely be a correct implementation and some convenience 
functions to make this even easier to use.

In order to decouple things, we need to use composition. This is what is 
already done: the qtlets are held in a dict at the instance level. A change in 
the attribute is signalled to the appropriate qtlets. This way, we don't have
to force our class to somehow be aware of the whole Qt metaobject machinery
(I think that's how it's called...).

Currently, the signalling is done using the `observe` mechanism in `trailets`.
It works, but it forces client code to use `traitlets`. This provides an
unacceptable constrait: you can't use properties, which are used all the time
when interfacing instruments. It also forces a rewrite of the class we want to
use. `Traitlets` uses metaclasses and descriptors. This is heavy stuff, we 
don't do that. It will ruin our lives at some point (metclass conflicts...). 
Therefore, we want to redesign the current basic example using something else.

We want to catch `__setattr__` and use it to signal a value change to the
widgets. If the attribute setting fails, we need to resync the widgets. 
Later, we may want to hijack the `__getattribute__` call to proceed using Qt's
thread mechanism.

There are two main ways to proceed about this. We can use a Mixin or decorators.

## Mixins 
Mixins would ideally be at the start of the MRO, and simply add basic behavior
to attribute setting and getting.

Pros:
- Inheritance is common.
- Preserve `isinstance` etc. This will be transparent with most code.
- This may change the class of things, we have to be careful to avoid
  changing the classes of all instances.
- We can't add too many methods, otherwise we could run into name conflicts. 

Cons:
- MRO tends to push things back when using multiple inheritance, not forward.
  (`__subclass_init__` is something new that may save us)
- We would like to be able to decorate single instances, not always entire
  classes.
  
## Decorators
Pros:
- Can wrap individual instances or entire classes. Less risks of side-effects.
- Less likely to run into conflicts. 

Cons:
- The magic sometimes gets out of hand.
- Simple wrappers don't preserve type, so we have to be extra careful there.
  It risks breaking code.


## Libraries:

**traitlets**: typed attributes, including validation and observe. https://github.com/ipython/traitlets

**traittypes**: extension of traitlets to include numerical data types. https://github.com/jupyter-widgets/traittypes

**qtconsole**: Frontend for IPython. Manages to stick together `QObject` and `HasTraits`. 
See `util.MetaQObjectHasTraits` and friends. https://github.com/jupyter/qtconsole

**spectacte**: https://github.com/rmorshea/spectate

Other documents:
**Descriptor protocol**: https://docs.python.org/3/howto/descriptor.html
