from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol
from .accept import Accept

class Visitor(Protocol):
    def visitTypeExprBin(self, obj: "TypeExprBin") -> None: ...
    def visitTypeExprRefBottomUp(self, obj: "TypeExprRefBottomUp") -> None: ...
    def visitTypeExprRefTopDown(self, obj: "TypeExprRefTopDown") -> None: ...
    def visitTypeExprFieldRef(self, obj: "TypeExprFieldRef") -> None: ...

class Accept(Protocol):
    def accept(self, v: Visitor) -> None: ...

class TypeExpr(Accept):
    pass

class TypeExprBin(ABC, Accept):
    @property
    @abstractmethod
    def left(self) -> str:
        ...
    @property
    @abstractmethod
    def right(self) -> str:
        ...
    @property
    @abstractmethod
    def op(self) -> str:
        ...

class TypeExprRefBottomUp(ABC, Accept):
    @property
    @abstractmethod
    def ref(self) -> str:
        ...

class TypeExprRefTopDown(ABC, Accept):
    @property
    @abstractmethod
    def ref(self) -> str:
        ...

class TypeExprFieldRef(ABC, Accept):
    @property
    @abstractmethod
    def field(self) -> str:
        ...
