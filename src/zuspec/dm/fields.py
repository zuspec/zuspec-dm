
from __future__ import annotations
import abc
from typing import Optional
from .accept import Accept
from .data_type import DataType
from .loc import Locatable
from .bindset import BindSet

class TypeField(Locatable):

    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @property
    @abc.abstractmethod
    def dataType(self) -> DataType: ...

    @property
    @abc.abstractmethod
    def bindSet(self) -> Optional[BindSet]: ...

class TypeFieldInOut(TypeField):

    @property
    @abc.abstractmethod
    def isOutput(self) -> bool: ...

