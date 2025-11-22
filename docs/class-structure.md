
# Zuspec Datamodel Class Structure

The Zuspec datamodel package uses several specific conventions to minimize
the code required to capture data structures and visitors. 

All members of the data model (ie not helper classes) must be dataclasses
and must implement `BaseP` -- typically by inheriting from `Base`. 
Each data-model class must support two key methods defined by the `BaseP`
protocol:
- accept -- Calls the appropriate visitor method for this type
- visitDefault -- Visits each relevant sub-field of the class

The `Base` class provides default implementations of this methods using
introspection.


Data model types are organized into `Profiles`. A profile consists of a 
package and all classes that implement `BaseP` within that package. Each profile
must be registered once by calling `profile(__name__)`. Each Python package
defines, at most, one profile.

Visitor classes are profile-specific. A visitor that is a dataclass should 
use the `visitor_dataclass` decorator. A visitor that is not a dataclass
should use the `visitor` decorator. In both cases, the relevant profile
package reference must be passed to the decorator.

```python
import zuspec.dm as dm

@dm.visitor_dataclass(dm)
class MyVisitor(dm.Visitor):

    def visitComponent(self, o : dm.Component):
        ...

```

An example of a dataclass visitor is shown above. Note that it inherits from
the datamodel Visitor class and applies the proper visitor.

Visitor classes 