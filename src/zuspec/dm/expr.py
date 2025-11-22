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
from .base import Base
import abc
import enum
from abc import ABC, abstractmethod
from typing import Optional, Protocol, TYPE_CHECKING
from .accept import Accept
from .loc import Loc

if TYPE_CHECKING:
    from .visitor import Visitor

@dc.dataclass(kw_only=True)
class Expr(Base): pass

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

@dc.dataclass(kw_only=True)
class ExprBin(Expr):
    lhs : Expr = dc.field()
    op : BinOp = dc.field()
    rhs : Expr = dc.field()

@dc.dataclass(kw_only=True)
class ExprRef(Expr): ...

@dc.dataclass
class TypeExprRefSelf(ExprRef): 
    """Reference to 'self'"""
    ...

@dc.dataclass(kw_only=True)
class ExprRefField(ExprRef):
    """Reference to a field relative to the base expression"""
    base : Expr = dc.field()
    index : int = dc.field()


@dc.dataclass(kw_only=True)
class ExprRefPy(ExprRef):
    """Reference relative to a Python object (base)"""
    base : Expr = dc.field()
    ref : str = dc.field()

class ExprRefBottomUp(ExprRef):
    """Reference to a field relative to the active procedural scope"""
    uplevel : int = dc.field(default=0)
    index : int = dc.field()

class TypeExprRefTopDown(ABC, Accept):
    @property
    @abstractmethod
    def ref(self) -> str:
        ...

