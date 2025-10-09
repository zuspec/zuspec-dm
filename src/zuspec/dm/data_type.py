from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Protocol, TYPE_CHECKING, Iterator
from .accept import Accept
from .bindset import BindSet
from .exec import Exec

if TYPE_CHECKING:
    from .fields import TypeField

class DataType(Accept): ...

class DataTypeBitVector(DataType):

    @property
    @abstractmethod
    def width(self) -> int: ...

class DataTypeBit(DataType):

    @property
    @abstractmethod
    def bits(self) -> int: ...

class DataTypeInt(DataType):

    @property
    @abstractmethod
    def bits(self) -> int: ...

class DataTypeExtern(DataType):

    @property
    @abstractmethod
    def name(self) -> str: ...

class DataTypeStruct(DataType):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def leafname(self) -> str: ...

    @property
    @abstractmethod
    def fields(self) -> Iterator[TypeField]:
        ...

    @property
    @abstractmethod
    def numFields(self) -> int:
        ...

    @abstractmethod
    def getField(self, i : int) -> TypeField:
        ...

    @abstractmethod
    def addField(self, f : TypeField) -> None:
        ...

    @property
    @abstractmethod
    def bindset(self) -> Optional[BindSet]: ...

    @abstractmethod
    def setBindset(self, b : BindSet) -> None: ...

    @property
    @abstractmethod
    def execs(self) -> Iterator[Exec]: ...

    @property
    @abstractmethod
    def numExecs(self) -> int: ...

    @abstractmethod
    def getExec(self, i : int) -> Exec: ...

    @abstractmethod
    def addExec(self, e : Exec) -> None: ...


class DataTypeComponent(DataTypeStruct):
    ...

class DataTypeExpr(Accept):
    @property
    @abstractmethod
    def expr_type(self) -> str:
        ...

class DataTypeArray(DataType):

    @property
    @abstractmethod
    def element_type(self) -> str:
        ...

class DataTypeBool(DataType):
    @property
    @abstractmethod
    def value(self) -> bool:
        ...

class DataTypeEnum(DataType):

    @property
    @abstractmethod
    def enum_type(self) -> str:
        ...

class DataTypeList(DataType):
    @property
    @abstractmethod
    def element_type(self) -> str:
        ...

class DataTypePtr(DataType):
    @property
    @abstractmethod
    def ref_type(self) -> str:
        ...

class DataTypeRef(DataType):

    @property
    @abstractmethod
    def ref_type(self) -> str:
        ...

class DataTypeString(DataType):
    @property
    @abstractmethod
    def value(self) -> str:
        ...

class TypeConstraint(Accept):
    pass

class TypeConstraintBlock(TypeConstraint):
    @property
    @abstractmethod
    def constraints(self) -> list[TypeConstraint]:
        ...

class TypeConstraintExpr(TypeConstraint):
    @property
    @abstractmethod
    def expr(self) -> str:
        ...

class TypeConstraintIfElse(Accept):
    @property
    @abstractmethod
    def condition(self) -> str:
        ...
    @property
    @abstractmethod
    def if_true(self) -> str:
        ...
    @property
    @abstractmethod
    def if_false(self) -> str:
        ...
