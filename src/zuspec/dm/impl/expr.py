from __future__ import annotations
from zuspec.dm.expr import (
    TypeExprBin,
    TypeExprRefBottomUp,
    TypeExprRefTopDown,
    TypeExprFieldRef,
    Visitor
)

class TypeExprBinImpl(TypeExprBin):
    def __init__(self, left: str, right: str, op: str) -> None:
        self._left = left
        self._right = right
        self._op = op

    @property
    def left(self) -> str:
        return self._left

    @property
    def right(self) -> str:
        return self._right

    @property
    def op(self) -> str:
        return self._op

    def accept(self, v: Visitor) -> None:
        v.visitTypeExprBin(self)

class TypeExprRefBottomUpImpl(TypeExprRefBottomUp):
    def __init__(self, ref: str) -> None:
        self._ref = ref

    @property
    def ref(self) -> str:
        return self._ref

    def accept(self, v: Visitor) -> None:
        v.visitTypeExprRefBottomUp(self)

class TypeExprRefTopDownImpl(TypeExprRefTopDown):
    def __init__(self, ref: str) -> None:
        self._ref = ref

    @property
    def ref(self) -> str:
        return self._ref

    def accept(self, v: Visitor) -> None:
        v.visitTypeExprRefTopDown(self)

class TypeExprFieldRefImpl(TypeExprFieldRef):
    def __init__(self, field: str) -> None:
        self._field = field

    @property
    def field(self) -> str:
        return self._field

    def accept(self, v: Visitor) -> None:
        v.visitTypeExprFieldRef(self)
