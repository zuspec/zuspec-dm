
from __future__ import annotations
import abc
from .accept import Accept
from .data_type import DataType

class TypeField(Accept):

    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @property
    @abc.abstractmethod
    def dataType(self) -> DataType: ...

class TypeFieldInOut(TypeField):

    @property
    @abc.abstractmethod
    def isOutput(self) -> bool: ...

