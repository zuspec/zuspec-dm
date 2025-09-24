from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol
from .accept import Accept

class DataType(Accept): ...

class DataTypeBitVector(DataType):

    @property
    @abstractmethod
    def width(self) -> int: ...


class DataTypeStruct(DataType):
    @property
    @abstractmethod
    def fields(self) -> list[str]:
        ...

class DataTypeExpr(ABC, Accept):
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

class TypeConstraintIfElse(ABC, Accept):
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
