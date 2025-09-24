from __future__ import annotations
from .data_type import (
    DataTypeBitVectorImpl, DataTypeStructImpl, DataTypeExprImpl,
    DataTypeBitVector, DataTypeStruct, DataTypeExpr, DataTypeArray, DataTypeBool
)

class Context:
    def mkDataTypeBitVector(self, width: int) -> DataTypeBitVector:
        return DataTypeBitVectorImpl(width)

    def mkDataTypeStruct(self, fields: list[str]) -> DataTypeStruct:
        return DataTypeStructImpl(fields)

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

    def mkTypeConstraintBlock(self, constraints: list[str]) -> TypeConstraintBlock:
        from zuspec.dm.impl.data_type import TypeConstraintBlockImpl
        return TypeConstraintBlockImpl(constraints)

    def mkTypeConstraintExpr(self, expr: str) -> TypeConstraintExpr:
        from zuspec.dm.impl.data_type import TypeConstraintExprImpl
        return TypeConstraintExprImpl(expr)

    def mkTypeConstraintIfElse(self, condition: str, if_true: str, if_false: str) -> TypeConstraintIfElse:
        from zuspec.dm.impl.data_type import TypeConstraintIfElseImpl
        return TypeConstraintIfElseImpl(condition, if_true, if_false)

    def mkTypeExprBin(self, left: str, right: str, op: str) -> TypeExprBin:
        from zuspec.dm.impl.expr import TypeExprBinImpl
        return TypeExprBinImpl(left, right, op)

    def mkTypeExprRefBottomUp(self, ref: str) -> TypeExprRefBottomUp:
        from zuspec.dm.impl.expr import TypeExprRefBottomUpImpl
        return TypeExprRefBottomUpImpl(ref)

    def mkTypeExprRefTopDown(self, ref: str) -> TypeExprRefTopDown:
        from zuspec.dm.impl.expr import TypeExprRefTopDownImpl
        return TypeExprRefTopDownImpl(ref)

    def mkTypeExprFieldRef(self, field: str) -> TypeExprFieldRef:
        from zuspec.dm.impl.expr import TypeExprFieldRefImpl
        return TypeExprFieldRefImpl(field)
