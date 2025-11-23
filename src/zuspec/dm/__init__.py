import dataclasses as dc
from typing import dataclass_transform

def profile(modname, super=None):
    """Register a profile"""
    from .profile_rgy import ProfileRgy
    ProfileRgy.register_profile(modname, super)


from .base import Base, BaseP
from .visitor import Visitor

@dataclass_transform()
def visitor_dataclass(pmod, *args, **kwargs):
    """Decorator for datamodel Visitor class"""
    def closure(T):
        c = dc.dataclass(T, *args, **kwargs)
        setattr(c, "__new__", lambda cls,pmod=pmod: Visitor.__new__(cls,pmod))
        return c
    return closure

def visitor(pmod, *args, **kwargs):
    """Decorator for non-datamodel Visitor class"""
    def closure(T):
        setattr(T, "__new__", lambda cls,pmod=pmod: Visitor.__new__(cls,pmod))
        return T
    return closure



# Re-export data model types
from .fields import Bind, BindSet, Field, FieldInOut
from .data_type import (
    DataType, DataTypeInt, DataTypeStruct, DataTypeClass, DataTypeComponent,
    DataTypeExpr, DataTypeEnum, DataTypeString
)
from .expr import (
    Expr, BinOp, UnaryOp, BoolOp, CmpOp, AugOp,
    ExprBin, ExprRef, ExprConstant, TypeExprRefSelf, ExprRefField, ExprRefPy,
    ExprRefBottomUp, TypeExprRefTopDown, ExprUnary, ExprBool, ExprCompare,
    ExprAttribute, ExprSlice, ExprSubscript, ExprCall, Keyword
)
from .expr_phase2 import (
    ExprList, ExprTuple, ExprDict, ExprSet, Comprehension, ExprListComp,
    ExprDictComp, ExprSetComp, ExprGeneratorExp, ExprIfExp, ExprLambda, ExprNamedExpr,
    ExprJoinedStr, ExprFormattedValue
)
from .stmt import (
    Stmt, StmtExpr, StmtAssign, StmtAugAssign, StmtReturn, StmtIf, StmtFor,
    StmtWhile, StmtBreak, StmtContinue, StmtPass, StmtRaise, StmtAssert, Alias, Arg, Arguments,
    WithItem, StmtWith, StmtExceptHandler, StmtTry, TypeIgnore, Module,
    StmtMatch, StmtMatchCase, Pattern, PatternValue, PatternAs, PatternOr, PatternSequence
)

__all__ = [
    "profile","Base","BaseP","Visitor",
    "Bind","BindSet","Field","FieldInOut",
    "DataType","DataTypeInt","DataTypeStruct","DataTypeClass","DataTypeComponent",
    "DataTypeExpr","DataTypeEnum","DataTypeString",
    "Expr","BinOp","UnaryOp","BoolOp","CmpOp","AugOp","ExprBin","ExprRef","ExprConstant",
    "TypeExprRefSelf","ExprRefField","ExprRefPy","ExprRefBottomUp","TypeExprRefTopDown","ExprUnary",
    "ExprBool","ExprCompare","ExprAttribute","ExprSlice","ExprSubscript","ExprCall","Keyword",
    "Stmt","StmtExpr","StmtAssign","StmtAugAssign","StmtReturn","StmtIf","StmtFor","StmtWhile",
    "StmtBreak","StmtContinue","StmtPass","StmtRaise","StmtAssert","Alias","Arg","Arguments",
"ExprList","ExprTuple","ExprDict","ExprSet","Comprehension","ExprListComp","ExprDictComp",
"ExprSetComp","ExprGeneratorExp","ExprIfExp","ExprLambda","ExprNamedExpr",
"WithItem","StmtWith","StmtExceptHandler","StmtTry","TypeIgnore","Module",
"ExprJoinedStr","ExprFormattedValue","StmtMatch","StmtMatchCase","Pattern","PatternValue","PatternAs","PatternOr","PatternSequence"
]

# Important to place after all data-model classes have been imported
profile(__name__)
