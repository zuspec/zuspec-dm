from __future__ import annotations
import dataclasses as dc
from typing import List, Iterator
from ..data_type import (
    DataType,
    DataTypeBit,
    DataTypeInt,
    DataTypeBitVector,
    DataTypeComponent,
    DataTypeStruct,
    DataTypeExpr,
    DataTypeArray,
    DataTypeBool,
    DataTypeEnum,
    DataTypeList,
    DataTypePtr,
    DataTypeRef,
    DataTypeString,
    TypeConstraintBlock,
    TypeConstraintExpr,
    TypeConstraintIfElse,
)
from .fields import TypeField, TypeFieldInOut

from ..visitor import Visitor

class DataTypeBitVectorImpl(DataTypeBitVector):
    def __init__(self, width: int) -> None:
        self._width = width

    @property
    def width(self) -> int:
        return self._width

    def accept(self, v: Visitor) -> None:
        v.visitDataTypeBitVector(self)

@dc.dataclass
class DataTypeBitImpl(DataTypeBit):
    _bits : int = dc.field()

    @property
    def bits(self) -> int:
        return self._bits
    
    def accept(self, v : Visitor) -> None:
        v.visitDataTypeBit(self)

@dc.dataclass
class DataTypeIntImpl(DataTypeInt):
    _bits : int = dc.field()

    @property
    def bits(self) -> int:
        return self._bits

    def accept(self, v : Visitor) -> None:
        v.visitDataTypeInt(self)

@dc.dataclass
class DataTypeStructImpl(DataTypeStruct):
    _name : str = dc.field()
    _fields : List[TypeField] = dc.field(default_factory=list)

    @property
    def name(self) -> str:
        return self._name

    @property
    def fields(self) -> Iterator[TypeField]:
        return self._fields.__iter__()
    
    def numFields(self):
        return len(self._fields)
    
    def getField(self, i):
        return self._fields[i]
    
    def addField(self, f):
        self._fields.append(f)

    def accept(self, v: Visitor) -> None:
        v.visitDataTypeStruct(self)

@dc.dataclass
class DataTypeComponentImpl(DataTypeComponent, DataTypeStructImpl):

    @property
    def name(self) -> str:
        return self._name
    pass

class DataTypeExprImpl(DataTypeExpr):
    def __init__(self, expr_type: str) -> None:
        self._expr_type = expr_type

    @property
    def expr_type(self) -> str:
        return self._expr_type

    def accept(self, v: Visitor) -> None:
        v.visitDataTypeExpr(self)

class DataTypeArrayImpl(DataTypeArray):
    def __init__(self, element_type: str) -> None:
        self._element_type = element_type

    @property
    def element_type(self) -> str:
        return self._element_type

    def accept(self, v: Visitor) -> None:
        v.visitDataTypeArray(self)

class DataTypeBoolImpl(DataTypeBool):
    def __init__(self, value: bool) -> None:
        self._value = value

    @property
    def value(self) -> bool:
        return self._value

    def accept(self, v: Visitor) -> None:
        v.visitDataTypeBool(self)

class DataTypeEnumImpl(DataTypeEnum):
    def __init__(self, enum_type: str) -> None:
        self._enum_type = enum_type

    @property
    def enum_type(self) -> str:
        return self._enum_type

    def accept(self, v: Visitor) -> None:
        v.visitDataTypeEnum(self)

class DataTypeListImpl(DataTypeList):
    def __init__(self, element_type: str) -> None:
        self._element_type = element_type

    @property
    def element_type(self) -> str:
        return self._element_type

    def accept(self, v: Visitor) -> None:
        v.visitDataTypeList(self)

class DataTypePtrImpl(DataTypePtr):
    def __init__(self, ref_type: str) -> None:
        self._ref_type = ref_type

    @property
    def ref_type(self) -> str:
        return self._ref_type

    def accept(self, v: Visitor) -> None:
        v.visitDataTypePtr(self)

class DataTypeRefImpl(DataTypeRef):
    def __init__(self, ref_type: str) -> None:
        self._ref_type = ref_type

    @property
    def ref_type(self) -> str:
        return self._ref_type

    def accept(self, v: Visitor) -> None:
        v.visitDataTypeRef(self)

class DataTypeStringImpl(DataTypeString):
    def __init__(self, value: str) -> None:
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def accept(self, v: Visitor) -> None:
        v.visitDataTypeString(self)

class TypeConstraintBlockImpl(TypeConstraintBlock):
    def __init__(self, constraints: list[str]) -> None:
        self._constraints = constraints

    @property
    def constraints(self) -> list[str]:
        return self._constraints

    def accept(self, v: Visitor) -> None:
        v.visitTypeConstraintBlock(self)

class TypeConstraintExprImpl(TypeConstraintExpr):
    def __init__(self, expr: str) -> None:
        self._expr = expr

    @property
    def expr(self) -> str:
        return self._expr

    def accept(self, v: Visitor) -> None:
        v.visitTypeConstraintExpr(self)

class TypeConstraintIfElseImpl(TypeConstraintIfElse):
    def __init__(self, condition: str, if_true: str, if_false: str) -> None:
        self._condition = condition
        self._if_true = if_true
        self._if_false = if_false

    @property
    def condition(self) -> str:
        return self._condition

    @property
    def if_true(self) -> str:
        return self._if_true

    @property
    def if_false(self) -> str:
        return self._if_false

    def accept(self, v: Visitor) -> None:
        v.visitTypeConstraintIfElse(self)

from zuspec.dm.data_type import DataTypeBitVector
from zuspec.dm.visitor import Visitor

class DataTypeBitVectorImpl(DataTypeBitVector):
    def __init__(self, width: int) -> None:
        self._width = width

    @property
    def width(self) -> int:
        return self._width

    def accept(self, v: Visitor) -> None:
        v.visitDataTypeBitVector(self)
