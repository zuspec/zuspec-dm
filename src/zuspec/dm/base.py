from __future__ import annotations
import dataclasses as dc
from typing import TYPE_CHECKING, Protocol, cast, runtime_checkable, Optional, Any

if TYPE_CHECKING:
    from .visitor import Visitor

@dc.dataclass
class Loc(object):
    file : Optional[str] = dc.field()
    line : int = dc.field()
    pos : int = dc.field()
    ref : Optional[Any] = dc.field(default=None)

@runtime_checkable
class BaseP(Protocol):

    def visitDefault(self, v : Visitor): ...

    def accept(self, v : Visitor): ...

    def getLoc(self) -> Optional[Loc]: ...


@dc.dataclass(kw_only=True)
class Base(BaseP):
    loc : Optional[Loc] = dc.field(default=None)

    def visitDefault(self, v : Visitor):
        print("visitDefault")

        # Handle bases first
        for b in type(self).__bases__:
            if issubclass(b, BaseP):
                getattr(v, "visit%s" % b.__name__)(self)

        # Iterate through the fields and dynamically handle
        for f in dc.fields(self):
            o = getattr(self, f.name)
            if f.type in [int, str]:
                pass
            elif isinstance(f.type, type):
                if issubclass(f.type, list):
                    pass
                elif issubclass(f.type, Base):
                    if o is not None:
                        cast(BaseP, o).accept(v)
            pass
        pass

    def accept(self, v : Visitor):
        getattr(v, "visit%s" % type(self).__name__)(self)

    def getLoc(self) -> Optional[Loc]:
        return self.loc
