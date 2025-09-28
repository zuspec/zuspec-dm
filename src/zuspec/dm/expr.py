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
import abc
import enum
from abc import ABC, abstractmethod
from typing import Optional, Protocol
from .accept import Accept
from .srcinfo import SrcInfo

class Visitor(Protocol):
    def visitTypeExprBin(self, obj: "TypeExprBin") -> None: ...
    def visitTypeExprRefBottomUp(self, obj: "TypeExprRefBottomUp") -> None: ...
    def visitTypeExprRefTopDown(self, obj: "TypeExprRefTopDown") -> None: ...
    def visitTypeExprFieldRef(self, obj: "TypeExprFieldRef") -> None: ...

class Accept(Protocol):
    def accept(self, v: Visitor) -> None: ...

class TypeExpr(Accept):

    @property
    @abc.abstractmethod
    def loc(self) -> Optional[SrcInfo]: ...

class BinOp(enum.Enum):
    Add = enum.auto()
    Sub = enum.auto()
    Mult = enum.auto()
    Div = enum.auto()
    Mod = enum.auto()
    BitAnd = enum.auto()
    BitOr = enum.auto()
    BitXor = enum.auto()
    LShift = enum.auto()
    RShift = enum.auto()
    Eq = enum.auto()
    NotEq = enum.auto()
    Lt = enum.auto()
    LtE = enum.auto()
    Gt = enum.auto()
    GtE = enum.auto()
    And = enum.auto()
    Or = enum.auto()

class TypeExprBin(ABC, Accept):
    @property
    @abstractmethod
    def lhs(self) -> TypeExpr: ...

    @property
    @abstractmethod
    def rhs(self) -> TypeExpr: ...

    @property
    @abstractmethod
    def op(self) -> BinOp: ...

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
