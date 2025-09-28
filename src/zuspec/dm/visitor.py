from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .data_type import (
        DataTypeBitVector, DataTypeStruct, DataTypeExpr, DataTypeArray, DataTypeBool,
        DataTypeEnum, DataTypeList, DataTypePtr, DataTypeRef, DataTypeString,
        TypeConstraintBlock, TypeConstraintExpr, TypeConstraintIfElse,
        DataType, DataTypeBit, DataTypeInt, DataTypeExtern, DataTypeComponent
    )
    from .expr import TypeExprBin, TypeExprRefBottomUp, TypeExprRefTopDown, TypeExprFieldRef
    from .fields import TypeField, TypeFieldInOut

class Visitor:

    def visitDataType(self, obj : DataType) -> None:
        pass

    def visitDataTypeBit(self, obj : DataTypeBit) -> None:
        self.visitDataType(obj)

    def visitDataTypeInt(self, obj : DataTypeInt) -> None:
        self.visitDataType(obj)

    def visitDataTypeComponent(self, obj : DataTypeComponent) -> None:
        self.visitDataTypeStruct(obj)

    def visitDataTypeExtern(self, obj : DataTypeExtern) -> None:
        self.visitDataType(obj)

    def visitDataTypeBitVector(self, obj: "DataTypeBitVector") -> None:
        pass

    def visitDataTypeStruct(self, obj: "DataTypeStruct") -> None:
        pass

    def visitDataTypeExpr(self, obj: "DataTypeExpr") -> None:
        pass

    def visitDataTypeArray(self, obj: "DataTypeArray") -> None:
        pass

    def visitDataTypeBool(self, obj: "DataTypeBool") -> None:
        pass

    def visitDataTypeEnum(self, obj: "DataTypeEnum") -> None:
        pass

    def visitDataTypeList(self, obj: "DataTypeList") -> None:
        pass

    def visitDataTypePtr(self, obj: "DataTypePtr") -> None:
        pass

    def visitDataTypeRef(self, obj: "DataTypeRef") -> None:
        pass

    def visitDataTypeString(self, obj: "DataTypeString") -> None:
        pass

    def visitTypeConstraintBlock(self, obj: "TypeConstraintBlock") -> None:
        pass

    def visitTypeConstraintExpr(self, obj: "TypeConstraintExpr") -> None:
        pass

    def visitTypeConstraintIfElse(self, obj: "TypeConstraintIfElse") -> None:
        pass

    def visitTypeExprBin(self, obj: "TypeExprBin") -> None:
        pass

    def visitTypeExprRefBottomUp(self, obj: "TypeExprRefBottomUp") -> None:
        pass

    def visitTypeExprRefTopDown(self, obj: "TypeExprRefTopDown") -> None:
        pass

    def visitTypeExprFieldRef(self, obj: "TypeExprFieldRef") -> None:
        pass

    def visitTypeField(self, obj : TypeField) -> None:
        obj.dataType.accept(self)

    def visitTypeField(self, obj : TypeFieldInOut) -> None:
        self.visitTypeField(obj)

