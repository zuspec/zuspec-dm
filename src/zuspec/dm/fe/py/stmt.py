from __future__ import annotations
import dataclasses as dc
from typing import Optional, List

from ...stmt import (
    Stmt as _Stmt, StmtExpr, StmtAssign, StmtAugAssign, StmtReturn, StmtIf, StmtFor,
    StmtWhile, StmtBreak, StmtContinue, StmtPass, StmtRaise, StmtAssert,
    WithItem, StmtWith, StmtExceptHandler, StmtTry, TypeIgnore, Module,
    StmtMatch, StmtMatchCase, Pattern, PatternValue, PatternAs, PatternOr, PatternSequence
)
from ...expr import Expr, AugOp

Stmt = _Stmt

# Re-expose and leave room for future additions (FunctionDef, imports, etc.)
