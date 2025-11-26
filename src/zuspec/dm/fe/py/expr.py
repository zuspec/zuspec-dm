from __future__ import annotations
import dataclasses as dc
import enum
from typing import Optional

from ...expr import (
    Expr as _Expr, BinOp, UnaryOp, BoolOp, CmpOp, AugOp,
    ExprBin, ExprUnary, ExprBool, ExprCompare, ExprConstant,
    ExprAttribute, ExprSlice, ExprSubscript as _ExprSubscript, ExprCall, Keyword
)
from ...expr_phase2 import (
    ExprList, ExprTuple, ExprDict, ExprSet,
    ExprListComp, ExprDictComp, ExprSetComp, ExprGeneratorExp,
    ExprIfExp, ExprLambda, ExprNamedExpr,
    ExprJoinedStr, ExprFormattedValue
)

Expr = _Expr

class ExprContext(enum.Enum):
    Load = enum.auto(); Store = enum.auto(); Del = enum.auto()

@dc.dataclass(kw_only=True)
class ExprName(Expr):
    id: str = dc.field()
    ctx: ExprContext = dc.field()

# Subscript is already present; re-expose under fe.py
class ExprSubscript(_ExprSubscript):
    pass

@dc.dataclass(kw_only=True)
class ExprStarred(Expr):
    value: Expr = dc.field()
    ctx: ExprContext = dc.field()
