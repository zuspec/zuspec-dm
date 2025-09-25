
from __future__ import annotations
import dataclasses as dc
from typing import TYPE_CHECKING
from ..fields import TypeField, TypeFieldInOut
from ..data_type import DataType

if TYPE_CHECKING:
    from ..visitor import Visitor

@dc.dataclass
class TypeFieldImpl(TypeField):
    _name : str = dc.field()
    _type : DataType = dc.field()

    @property
    def name(self) -> str:
        return self._name

    @property
    def dataType(self) -> DataType: 
        return self._type
    
    def accept(self, v : Visitor):
        v.visitTypeField(self)
    
@dc.dataclass
class TypeFieldInOutImpl(TypeFieldInOut, TypeFieldImpl):
    _is_out : bool = dc.field()

    @property
    def isOutput(self) -> bool: 
        return self._is_out