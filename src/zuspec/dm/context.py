
from __future__ import annotations
import abc
from typing import Iterator, Optional, List, Protocol, Iterator
from .bindset import Bind, BindSet
from .data_type import (
    DataType,
    DataTypeBitVector, DataTypeStruct, DataTypeExpr, DataTypeArray, 
    DataTypeBool, DataTypeEnum, DataTypeList, DataTypePtr, DataTypeRef,
    DataTypeString, DataTypeComponent,
    DataTypeBit, DataTypeInt, DataTypeExtern
)
from .exec import (
    Exec, ExecSync, ExecStmt, ExecStmtExpr, ExecStmtIf, ExecStmtIfElse, 
    ExecStmtAssign, ExecStmtScope
)
from .expr import (
    TypeExpr,
    BinOp,
    TypeExprRefField,
    TypeExprRefSelf,
    TypeExprBin,
    TypeExprRefPy
)
from .fields import (
    TypeField, TypeFieldInOut
)
from .loc import Loc

class Context(Protocol):

    @abc.abstractmethod
    def mkBind(self, lhs : Optional[TypeExpr], rhs : Optional[TypeExpr], loc : Optional[Loc] = None) -> Bind: ...

    @abc.abstractmethod
    def mkBindSet(self, binds : Optional[Iterator[Bind]] = None) -> BindSet: ...

    @abc.abstractmethod
    def addDataTypeStruct(self, t : DataTypeStruct): ...

    @abc.abstractmethod
    def findDataTypeStruct(self, name : str) -> Optional[DataTypeStruct]: ...

    @abc.abstractmethod
    def findDataTypeBit(self, sz : int, create : bool=True) -> Optional[DataTypeBit]: ...

    @abc.abstractmethod
    def findDataTypeInt(self, sz : int, create : bool=True) -> Optional[DataTypeInt]: ...

    @abc.abstractmethod
    def findDataTypeExtern(self, name : str, create : bool=True) -> Optional[DataTypeExtern]: ...

    @abc.abstractmethod
    def mkDataTypeBitVector(self, width: int) -> DataTypeBitVector: ...

    @abc.abstractmethod
    def mkDataTypeComponent(self, name : str) -> DataTypeComponent: ...

    @abc.abstractmethod
    def mkDataTypeStruct(self, name : str) -> DataTypeStruct: ...

    @abc.abstractmethod
    def mkDataTypeExpr(self, expr_type: str) -> DataTypeExpr: ...

    @abc.abstractmethod
    def mkDataTypeArray(self, element_type: str) -> DataTypeArray: ...

    @abc.abstractmethod
    def mkDataTypeBool(self, value: bool) -> DataTypeBool: ...

    @abc.abstractmethod
    def mkDataTypeEnum(self, enum_type: str) -> DataTypeEnum: ...

    @abc.abstractmethod
    def mkDataTypeList(self, element_type: str) -> DataTypeList: ...

    @abc.abstractmethod
    def mkDataTypePtr(self, ref_type: str) -> DataTypePtr: ...

    @abc.abstractmethod
    def mkDataTypeRef(self, ref_type: str) -> DataTypeRef: ...

    @abc.abstractmethod
    def mkDataTypeString(self, value: str) -> DataTypeString: ...

    @abc.abstractmethod
    def mkExecStmtExpr(self, expr : TypeExpr, loc : Optional[Loc] = None) -> ExecStmtExpr: ...

    @abc.abstractmethod
    def mkExecStmtAssign(self, targets : List[TypeExpr], value : TypeExpr, loc : Optional[Loc] = None) -> ExecStmtAssign: ...

    @abc.abstractmethod
    def mkExecStmtIf(self, cond : TypeExpr, stmt : ExecStmt, loc : Optional[Loc] = None) -> ExecStmtIf: ...

    @abc.abstractmethod
    def mkExecStmtIfElse(self, 
                         if_clauses : List[ExecStmtIf], 
                         else_clause : Optional[ExecStmt] = None,
                         loc : Optional[Loc] = None) -> ExecStmtIfElse: ...
    
    @abc.abstractmethod
    def mkExecStmtScope(self, loc : Optional[Loc] = None) -> ExecStmtScope: ...

    @abc.abstractmethod
    def mkExec(self,
                   ref : Optional[TypeExprRefPy] = None,
                   loc : Optional[Loc] = None) -> Exec: ...

    @abc.abstractmethod
    def mkExecSync(self, 
                   clock : TypeExpr, 
                   reset : TypeExpr, 
                   ref : Optional[TypeExprRefPy] = None,
                   loc : Optional[Loc] = None) -> ExecSync: ...

    @abc.abstractmethod
    def mkTypeConstraintBlock(self, constraints: list[str]) -> TypeConstraintBlock: ...

    @abc.abstractmethod
    def mkTypeConstraintExpr(self, expr: str) -> TypeConstraintExpr: ...

    @abc.abstractmethod
    def mkTypeConstraintIfElse(self, condition: str, if_true: str, if_false: str) -> TypeConstraintIfElse: ...

    @abc.abstractmethod
    def mkTypeExprBin(self, 
                      lhs: TypeExpr, 
                      op : BinOp, 
                      rhs: TypeExpr,
                      loc : Optional[Loc] = None) -> TypeExprBin: ...

    @abc.abstractmethod
    def mkTypeExprRefField(self, base : TypeExpr, index : int, loc : Optional[Loc] = None) -> TypeExprRefField: ...

    @abc.abstractmethod
    def mkTypeExprRefSelf(self, loc : Optional[Loc] = None) -> TypeExprRefSelf: ...

    @abc.abstractmethod
    def mkTypeExprRefPy(self, ref: str, loc : Optional[Loc] = None) -> TypeExprRefPy: ...

    @abc.abstractmethod
    def mkTypeExprRefBottomUp(self, ref: str) -> TypeExprRefBottomUp: ...

    @abc.abstractmethod
    def mkTypeExprRefTopDown(self, ref: str) -> TypeExprRefTopDown: ...

    @abc.abstractmethod
    def mkTypeExprFieldRef(self, field: str) -> TypeExprFieldRef: ...

    @abc.abstractmethod
    def mkTypeField(self, 
                    name : str, 
                    type : DataType,
                    binds : Optional[BindSet] = None,
                    loc : Optional[Loc] = None) -> TypeField: ...

    @abc.abstractmethod
    def mkTypeFieldInOut(self, name : str, type : DataType, is_out : bool) -> TypeFieldInOut: ...

