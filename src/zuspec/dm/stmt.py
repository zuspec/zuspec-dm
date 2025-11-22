from __future__ import annotations
import dataclasses as dc
from typing import Optional, List
from .base import Base
from .expr import Expr, AugOp

@dc.dataclass(kw_only=True)
class Alias(Base):
    name: str = dc.field()
    asname: Optional[str] = dc.field(default=None)

@dc.dataclass(kw_only=True)
class Arg(Base):
    arg: str = dc.field()
    annotation: Optional[Expr] = dc.field(default=None)

@dc.dataclass(kw_only=True)
class Arguments(Base):
    posonlyargs: List[Arg] = dc.field(default_factory=list)
    args: List[Arg] = dc.field(default_factory=list)
    vararg: Optional[Arg] = dc.field(default=None)
    kwonlyargs: List[Arg] = dc.field(default_factory=list)
    kw_defaults: List[Optional[Expr]] = dc.field(default_factory=list)
    kwarg: Optional[Arg] = dc.field(default=None)
    defaults: List[Expr] = dc.field(default_factory=list)

@dc.dataclass(kw_only=True)
class Stmt(Base):
    pass

@dc.dataclass(kw_only=True)
class StmtExpr(Stmt):
    expr: Expr = dc.field()

@dc.dataclass(kw_only=True)
class StmtAssign(Stmt):
    targets: List[Expr] = dc.field(default_factory=list)
    value: Expr = dc.field()

@dc.dataclass(kw_only=True)
class StmtAugAssign(Stmt):
    target: Expr = dc.field()
    op: AugOp = dc.field()
    value: Expr = dc.field()

@dc.dataclass(kw_only=True)
class StmtReturn(Stmt):
    value: Optional[Expr] = dc.field(default=None)

@dc.dataclass(kw_only=True)
class StmtIf(Stmt):
    test: Expr = dc.field()
    body: List[Stmt] = dc.field(default_factory=list)
    orelse: List[Stmt] = dc.field(default_factory=list)

@dc.dataclass(kw_only=True)
class StmtFor(Stmt):
    target: Expr = dc.field()
    iter: Expr = dc.field()
    body: List[Stmt] = dc.field(default_factory=list)
    orelse: List[Stmt] = dc.field(default_factory=list)

@dc.dataclass(kw_only=True)
class StmtWhile(Stmt):
    test: Expr = dc.field()
    body: List[Stmt] = dc.field(default_factory=list)
    orelse: List[Stmt] = dc.field(default_factory=list)

@dc.dataclass(kw_only=True)
class StmtBreak(Stmt):
    pass

@dc.dataclass(kw_only=True)
class StmtContinue(Stmt):
    pass

@dc.dataclass(kw_only=True)
class StmtPass(Stmt):
    pass

@dc.dataclass(kw_only=True)
class StmtRaise(Stmt):
    exc: Optional[Expr] = dc.field(default=None)
    cause: Optional[Expr] = dc.field(default=None)

@dc.dataclass(kw_only=True)
class StmtAssert(Stmt):
    test: Expr = dc.field()
    msg: Optional[Expr] = dc.field(default=None)
