
from __future__ import annotations
import dataclasses as dc
from typing import Optional, TYPE_CHECKING
from ..fields import TypeField, TypeFieldInOut
from ..data_type import DataType
from ..loc import Loc

if TYPE_CHECKING:
    from ..visitor import Visitor

@dc.dataclass
class TypeFieldImpl(TypeField):
    _name : str = dc.field()
    _type : DataType = dc.field()
    _loc : Optional[Loc] = dc.field(default=None)

    @property
    def name(self) -> str:
        return self._name

    @property
    def dataType(self) -> DataType: 
        return self._type

    @property
    def loc(self) -> Optional[Loc]:
        return self._loc

    def accept(self, v : Visitor):
        v.visitTypeField(self)
    
@dc.dataclass
class TypeFieldInOutImpl(TypeFieldInOut, TypeFieldImpl):
    _is_out : bool = dc.field(default=False)

    @property
    def isOutput(self) -> bool: 
        return self._is_out

    def accept(self, v : Visitor):
        v.visitTypeFieldInOut(self)