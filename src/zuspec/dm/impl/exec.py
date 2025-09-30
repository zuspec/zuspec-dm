
import dataclasses as dc
from typing import Iterator, List, Optional
from ..exec import (
    Exec, ExecStmt, ExecStmtAssign, ExecStmtExpr, ExecStmtScope, ExecSync,
    ExecStmtIf, ExecStmtIfElse
)
from .expr import TypeExpr
from ..loc import Loc
from ..visitor import Visitor

@dc.dataclass
class ExecStmtImpl(ExecStmt):
    _loc : Optional[Loc] = dc.field()

    @property
    def loc(self) -> Optional[Loc]:
        return self._loc

    def accept(self, v : Visitor):
        v.visitExecStmt(self)

@dc.dataclass
class ExecStmtExprImpl(ExecStmtExpr, ExecStmtImpl):
    _expr : TypeExpr = dc.field()

    @property
    def expr(self) -> TypeExpr:
        return self._expr
    
    def accept(self, v : Visitor):
        v.visitExecStmtExpr(self)

@dc.dataclass
class ExecStmtIfImpl(ExecStmtIf, ExecStmtImpl):
    _cond : Optional[TypeExpr] = dc.field(default=None)
    _stmt : Optional[ExecStmt] = dc.field(default=None)

    @property
    def cond(self) -> TypeExpr:
        if self._cond is None: raise Exception()
        return self._cond

    @property
    def stmt(self) -> ExecStmt:
        if self._stmt is None: raise Exception()
        return self._stmt

    def accept(self, v : Visitor) -> None:
        v.visitExecStmtIf(self)

@dc.dataclass
class ExecStmtIfElseImpl(ExecStmtIfElse,ExecStmtImpl):
    _if_clauses : List[ExecStmtIf] = dc.field(default_factory=list)
    _else_clause : Optional[ExecStmt] = dc.field(default=None)

    @property
    def if_clauses(self) -> Iterator[ExecStmtIf]:
        return iter(self._if_clauses)

    @property
    def else_clause(self) -> Optional[ExecStmt]:
        return self._else_clause
    
    def accept(self, v : Visitor) -> None:
        v.visitExecStmtIfElse(self)

@dc.dataclass
class ExecStmtAssignImpl(ExecStmtAssign, ExecStmtImpl):
    _value : TypeExpr = dc.field()
    _targets : List[TypeExpr] = dc.field(default_factory=list)

    @property
    def targets(self) -> Iterator[TypeExpr]:
        return iter(self._targets)

    @property
    def value(self) -> TypeExpr:
        return self._value

@dc.dataclass
class ExecStmtScopeImpl(ExecStmtScope, ExecStmtImpl):
    _stmts : List[ExecStmt] = dc.field(default_factory=list)

    @property
    def stmts(self) -> Iterator[ExecStmt]:
        return iter(self._stmts)

    @property
    def numStmts(self) -> int:
        return len(self._stmts)

    def getStmt(self, i : int) -> ExecStmt:
        return self._stmts[i]

    def addStmt(self, stmt : ExecStmt) -> None:
        self._stmts.append(stmt)
    
    def accept(self, v : Visitor) -> None:
        v.visitExecStmtScope(self)


@dc.dataclass
class ExecImpl(Exec):
    _stmts : List[ExecStmt] = dc.field(default_factory=list)
    _loc : Optional[Loc] = dc.field(default=None)

    @property
    def loc(self) -> Optional[Loc]:
        return self._loc

    @property
    def stmts(self) -> Iterator[ExecStmt]:
        return self._stmts.__iter__()

    def numStmts(self) -> int:
        return len(self._stmts)

    def addStmt(self, s : ExecStmt) -> None:
        self._stmts.append(s)

    def getStmt(self, i : int) -> ExecStmt:
        return self._stmts[i]
    
    def accept(self, v : Visitor) -> None:
        v.visitExec(self)

@dc.dataclass
class ExecSyncImpl(ExecSync,ExecImpl):
    _clock : Optional[TypeExpr] = dc.field(default=None)
    _reset : Optional[TypeExpr] = dc.field(default=None)

    @property
    def clock(self) -> TypeExpr:
        if self._clock is None: raise Exception("Clock cannot be None")
        return self._clock

    @property
    def reset(self) -> TypeExpr:
        if self._reset is None: raise Exception("Clock cannot be None")
        return self._reset

    def accept(self, v : Visitor) -> None:
        v.visitExecSync(self)
