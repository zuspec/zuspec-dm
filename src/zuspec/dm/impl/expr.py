#****************************************************************************
# Copyright 2019-2025 Matthew Ballance and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#****************************************************************************
from __future__ import annotations
import dataclasses as dc
from typing import Optional
from ..expr import (
    BinOp,
    TypeExpr,
    TypeExprBin,
    TypeExprRefBottomUp,
    TypeExprRefTopDown,
    TypeExprFieldRef
)
from ..loc import Loc
from ..visitor import Visitor

@dc.dataclass
class TypeExprImpl(TypeExpr):
    _loc : Optional[Loc] = dc.field()

@dc.dataclass
class TypeExprBinImpl(TypeExprBin,TypeExprImpl):
    _lhs : TypeExpr = dc.field()
    _op : BinOp = dc.field()
    _rhs : TypeExpr = dc.field()

    @property
    def left(self) -> TypeExpr:
        return self._lhs

    @property
    def right(self) -> TypeExpr:
        return self._rhs

    @property
    def op(self) -> BinOp:
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
