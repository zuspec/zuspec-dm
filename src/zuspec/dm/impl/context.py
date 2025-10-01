
from __future__ import annotations
import dataclasses as dc
from typing import Dict, List, Optional, Iterable
from ..context import Context as IContext
from ..data_type import (
    DataTypeEnum, DataTypeList, DataTypePtr, DataTypeRef,
    DataTypeString, DataTypeComponent,
    DataTypeBit, DataTypeInt, DataType, DataTypeExtern
)
from .data_type import (
    DataTypeBitVectorImpl, DataTypeStructImpl, DataTypeExprImpl,
    DataTypeBitVector, DataTypeStruct, DataTypeExpr, DataTypeArray, DataTypeBool,
    DataTypeComponentImpl, DataTypeBitImpl, DataTypeIntImpl,
    DataTypeExternImpl
)
from .exec import (
    Exec, ExecSync, ExecStmt, ExecStmtAssign, ExecStmtExpr, ExecStmtIf,
    ExecStmtIfElse, ExecStmtScope
)
from ..expr import (
    TypeExpr,
    BinOp,
    TypeExprBin,
    TypeExprRefPy
)
from .fields import (
    TypeField,
    TypeFieldInOut
)
from ..loc import Loc

@dc.dataclass
class Context(IContext):
    _struct_type_m : Dict[str,DataTypeStruct] = dc.field(default_factory=dict)
    _bit_type_m : Dict[int,DataTypeBit] = dc.field(default_factory=dict)
    _int_type_m : Dict[int,DataTypeInt] = dc.field(default_factory=dict)
    _ext_type_m : Dict[str,DataTypeExtern] = dc.field(default_factory=dict)

    def addDataTypeStruct(self, t : DataTypeStruct): 
        if t.name in self._struct_type_m.keys():
            raise Exception("Struct type %s already registered" % t.name)
        self._struct_type_m[t.name] = t

    def findDataTypeStruct(self, name : str) -> Optional[DataTypeStruct]:
        if name in self._struct_type_m.keys():
            return self._struct_type_m[name]
        else:
            return None
        
    def findDataTypeBit(self, sz, create = True) -> Optional[DataTypeBit]:
        if sz in self._bit_type_m.keys():
            return self._bit_type_m[sz]
        elif create:
            t = DataTypeBitImpl(sz)
            self._bit_type_m[sz] = t
            return t
        else:
            return None

    def findDataTypeInt(self, sz, create = True) -> Optional[DataTypeInt]:
        if sz in self._int_type_m.keys():
            return self._int_type_m[sz]
        elif create:
            t = DataTypeIntImpl(sz)
            self._int_type_m[sz] = t
            return t
        else:
            return None
        
    def findDataTypeExtern(self, name, create = True) -> Optional[DataTypeExtern]:
        if name in self._ext_type_m.keys():
            return self._ext_type_m[name]
        elif create:
            t = DataTypeExternImpl(name)
            self._ext_type_m[name] = t
            return t
        else:
            return None

    def mkDataTypeBitVector(self, width: int) -> DataTypeBitVector:
        return DataTypeBitVectorImpl(width)

    def mkDataTypeComponent(self, name : str) -> DataTypeComponent:
        return DataTypeComponentImpl(name)

    def mkDataTypeStruct(self, name : str) -> DataTypeStruct:
        return DataTypeStructImpl(name)

    def mkDataTypeExpr(self, expr_type: str) -> DataTypeExpr:
        return DataTypeExprImpl(expr_type)

    def mkDataTypeArray(self, element_type: str) -> DataTypeArray:
        from zuspec.dm.impl.data_type import DataTypeArrayImpl
        return DataTypeArrayImpl(element_type)

    def mkDataTypeBool(self, value: bool) -> DataTypeBool:
        from zuspec.dm.impl.data_type import DataTypeBoolImpl
        return DataTypeBoolImpl(value)

    def mkDataTypeEnum(self, enum_type: str) -> DataTypeEnum:
        from zuspec.dm.impl.data_type import DataTypeEnumImpl
        return DataTypeEnumImpl(enum_type)

    def mkDataTypeList(self, element_type: str) -> DataTypeList:
        from zuspec.dm.impl.data_type import DataTypeListImpl
        return DataTypeListImpl(element_type)

    def mkDataTypePtr(self, ref_type: str) -> DataTypePtr:
        from zuspec.dm.impl.data_type import DataTypePtrImpl
        return DataTypePtrImpl(ref_type)

    def mkDataTypeRef(self, ref_type: str) -> DataTypeRef:
        from zuspec.dm.impl.data_type import DataTypeRefImpl
        return DataTypeRefImpl(ref_type)

    def mkDataTypeString(self, value: str) -> DataTypeString:
        from zuspec.dm.impl.data_type import DataTypeStringImpl
        return DataTypeStringImpl(value)

    def mkExecStmtIf(self, cond : TypeExpr, stmt : ExecStmt, loc : Optional[Loc] = None) -> ExecStmtIf:
        from .exec import ExecStmtIfImpl
        return ExecStmtIfImpl(loc, cond, stmt)

    def mkExecStmtIfElse(self, 
                         if_clauses : List[ExecStmtIf], 
                         else_clause : Optional[ExecStmt] = None,
                         loc : Optional[Loc] = None) -> ExecStmtIfElse:
        from .exec import ExecStmtIfElseImpl
        return ExecStmtIfElseImpl(loc, if_clauses, else_clause)

    def mkExecStmtExpr(self, expr : TypeExpr, loc : Optional[Loc] = None) -> ExecStmtExpr:
        from .exec import ExecStmtExprImpl
        return ExecStmtExprImpl(loc, expr)

    def mkExecStmtAssign(self, targets : List[TypeExpr], value : TypeExpr, loc : Optional[Loc] = None) -> ExecStmtAssign:
        from .exec import ExecStmtAssignImpl
        return ExecStmtAssignImpl(loc, value, targets)

    def mkExecStmtScope(self, loc : Optional[Loc] = None) -> ExecStmtScope:
        from .exec import ExecStmtScopeImpl
        return ExecStmtScopeImpl(loc)

    def mkExec(self,
                   ref : Optional[TypeExprRefPy] = None,
                   loc : Optional[Loc] = None) -> Exec:
        from .exec import ExecImpl
        return ExecImpl(_loc=loc, _ref=ref)

    def mkExecSync(self, 
                   clock : TypeExpr, 
                   reset : TypeExpr, 
                   ref : Optional[TypeExprRefPy] = None,
                   loc : Optional[Loc] = None) -> ExecSync:
        from .exec import ExecSyncImpl
        return ExecSyncImpl(
            _loc=loc,
            _ref=ref,
            _clock=clock, _reset=reset)

    def mkTypeConstraintBlock(self, constraints: list[str]) -> TypeConstraintBlock:
        from zuspec.dm.impl.data_type import TypeConstraintBlockImpl
        return TypeConstraintBlockImpl(constraints)

    def mkTypeConstraintExpr(self, expr: str) -> TypeConstraintExpr:
        from zuspec.dm.impl.data_type import TypeConstraintExprImpl
        return TypeConstraintExprImpl(expr)

    def mkTypeConstraintIfElse(self, condition: str, if_true: str, if_false: str) -> TypeConstraintIfElse:
        from zuspec.dm.impl.data_type import TypeConstraintIfElseImpl
        return TypeConstraintIfElseImpl(condition, if_true, if_false)

    def mkTypeExprBin(self, 
                      lhs: TypeExpr, 
                      op : BinOp, 
                      rhs: TypeExpr,
                      loc : Optional[Loc]=None) -> TypeExprBin:
        from zuspec.dm.impl.expr import TypeExprBinImpl
        return TypeExprBinImpl(loc, lhs, op, rhs)

    def mkTypeExprRefPy(self, ref : str, loc : Optional[Loc] = None) -> TypeExprRefPy:
        from .expr import TypeExprRefPyImpl
        return TypeExprRefPyImpl(loc, ref)

    def mkTypeExprRefBottomUp(self, ref: str) -> TypeExprRefBottomUp:
        from zuspec.dm.impl.expr import TypeExprRefBottomUpImpl
        return TypeExprRefBottomUpImpl(ref)

    def mkTypeExprRefTopDown(self, ref: str) -> TypeExprRefTopDown:
        from zuspec.dm.impl.expr import TypeExprRefTopDownImpl
        return TypeExprRefTopDownImpl(ref)

    def mkTypeExprFieldRef(self, field: str) -> TypeExprFieldRef:
        from zuspec.dm.impl.expr import TypeExprFieldRefImpl
        return TypeExprFieldRefImpl(field)

    def mkTypeField(self, name : str, type : DataType) -> TypeField:
        from .fields import TypeFieldImpl
        return TypeFieldImpl(name, type)

    def mkTypeFieldInOut(self, name : str, type : DataType, is_out : bool) -> TypeFieldInOut:
        from .fields import TypeFieldInOutImpl
        return TypeFieldInOutImpl(name, type, is_out)
