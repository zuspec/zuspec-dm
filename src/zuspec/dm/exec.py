
import abc
from typing import Iterator, Optional
from .expr import TypeExpr, TypeExprRefPy
from .loc import Locatable

class ExecStmt(Locatable): ...

class ExecStmtExpr(ExecStmt):

    @property
    @abc.abstractmethod
    def expr(self) -> TypeExpr: ...

class ExecStmtAssign(ExecStmt):

    @property
    @abc.abstractmethod
    def targets(self) -> Iterator[TypeExpr]: ...

    @property
    @abc.abstractmethod
    def value(self) -> TypeExpr: ...

class ExecStmtIf(ExecStmt):

    @property
    @abc.abstractmethod
    def cond(self) -> TypeExpr: ...

    @property
    @abc.abstractmethod
    def stmt(self) -> ExecStmt: ...

class ExecStmtIfElse(ExecStmt):

    @property
    @abc.abstractmethod
    def if_clauses(self) -> Iterator[ExecStmtIf]: ...

    @property
    @abc.abstractmethod
    def else_clause(self) -> Optional[ExecStmt]: ...

class ExecStmtScope(ExecStmt):

    @property
    @abc.abstractmethod
    def stmts(self) -> Iterator[ExecStmt]: ...

    @property
    @abc.abstractmethod
    def numStmts(self) -> int: ...

    @abc.abstractmethod
    def getStmt(self, i : int) -> ExecStmt: ...

    @abc.abstractmethod
    def addStmt(self, stmt : ExecStmt) -> None: ...

class Exec(Locatable):

    @property
    @abc.abstractmethod
    def stmts(self) -> Iterator[ExecStmt]: ...

    @abc.abstractmethod
    def numStmts(self) -> int: ...

    @abc.abstractmethod
    def addStmt(stmt, s : ExecStmt) -> None: ...

    @abc.abstractmethod
    def getStmt(stmt, i : int) -> ExecStmt: ...

    @property
    @abc.abstractmethod
    def ref(self) -> Optional[TypeExprRefPy]: ...

class ExecSync(Exec):

    @property
    @abc.abstractmethod
    def clock(self) -> TypeExpr: ...

    @property
    @abc.abstractmethod
    def reset(self) -> TypeExpr: ...

    pass