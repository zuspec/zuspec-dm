# How to Add a New Data Model Class

This document standardizes the steps for adding a new data model (DM) class to the project. Follow this guide whenever introducing a new interface and its Python implementation.

Scope:
- Interfaces live under `src/zuspec/dm` (no implementation).
- Implementations live under `src/zuspec/dm/impl`.
- All objects must be created via the `Context` factory (`src/zuspec/dm/impl/context.py`).
- Add a Visitor method `visit<Type>` for every new interface.

Do not add types with “Model” in the name.

---

## 1) Identify scope and name

- Determine family:
  - `vsc` (e.g. `DataTypeInt`, `TypeExprBin`, `TypeConstraintBlock`)
  - `arl` (e.g. `TypeAction`, `TypeFieldReg`, `TypeProcStmtIfElse`, `DataTypeReg`)
- Determine category module:
  - vsc: `data_type.py`, `type_expr.py`, `constraint.py`, etc
  - arl: `type.py`, `type_field.py`, `proc_stmt.py`, `data_type.py`, etc
- Map to the original header (for traceability), ignoring any with “Model” in the name.

Record the mapping in a short comment or in docs (see Section 8).

---

## 2) Add the interface (no implementation)

- Add to the appropriate module:
  - `src/zuspec/dm/{vsc|arl}/{category}.py`
- Use Python ABCs or Protocols for the interface.
- Include an `accept(self, v: Visitor) -> None` method for Visitor dispatch.
- Keep properties minimal and read-only (`@property`). Implementation handles mutability.

Example:
```python
# python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol

class Visitor(Protocol):
    # Forward-declared; real Visitor is in src/zuspec/dm/visitor.py
    ...

class Accept(Protocol):
    def accept(self, v: Visitor) -> None: ...

class DataTypeFoo(ABC, Accept):
    @property
    @abstractmethod
    def name(self) -> str: ...
```

Export the new type in the package `__init__.py` files.

---

## 3) Extend the Visitor interface

- File: `src/zuspec/dm/visitor.py`
- Add a method: `def visit<Type>(self, obj: "<Type>") -> None: ...`
  - Example: `visitDataTypeFoo(self, obj: "DataTypeFoo") -> None`
- Use type-only imports and `from __future__ import annotations` to avoid cycles.

Example:
```python
# python
from __future__ import annotations
from abc import ABC, abstractmethod

class Visitor(ABC):
    @abstractmethod
    def visitDataTypeFoo(self, obj: "DataTypeFoo") -> None: ...
```

---

## 4) Add the implementation class

- File: `src/zuspec/dm/impl/{vsc|arl}/{category}.py`
- Implement the interface. Do not expose public constructors outside Context.
- Ensure `accept()` calls the matching visitor method.

Example:
```python
# python
from __future__ import annotations

class DataTypeFooImpl(DataTypeFoo):
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def accept(self, v: Visitor) -> None:
        v.visitDataTypeFoo(self)
```

---

## 5) Register a factory method in Context

- File: `src/zuspec/dm/impl/context.py`
- Add a `mk*` method that returns the interface type and constructs the implementation.
- All objects must be created via Context.

Example:
```python
# python
from __future__ import annotations

class Context:
    def mkDataTypeFoo(self, name: str) -> DataTypeFoo:
        return DataTypeFooImpl(name)
```

---

## 6) Update exports

- Add the new interface symbol to:
  - `src/zuspec/dm/{vsc|arl}/__init__.py`
  - `src/zuspec/dm/__init__.py`
- Add implementation symbols to:
  - `src/zuspec/dm/impl/__init__.py` (optional; usually Context is the only public impl entry).

---

## 7) Add unit tests

- Location suggestion: `tests/dm/{vsc|arl}/test_<category>_<type>.py`
- Verify:
  - Context factory returns the interface type.
  - `accept()` dispatches to the corresponding Visitor method.

Minimal pytest example:
```python
# python
from __future__ import annotations
from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.vsc.data_type import DataTypeFoo

class SpyVisitor(Visitor):
    def __init__(self) -> None:
        self.called = False
    def visitDataTypeFoo(self, obj: DataTypeFoo) -> None:
        self.called = True

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkDataTypeFoo("foo")
    assert isinstance(t, DataTypeFoo)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
```

---

## 8) Document mapping and API

In this document (or a dedicated per-type mapping file), record:
- Original header path (example): `packages/zuspec-arl-dm/src/include/zsp/arl/dm/IDataTypeReg.h`
- New interface path: `src/zuspec/dm/arl/data_type.py::DataTypeReg`
- Visitor method name: `visitDataTypeReg`
- Context factory name: `mkDataTypeReg(name: str, ...) -> DataTypeReg`

### Mapping: IDataTypeBitVector

- Original header path: `packages/vsc-dm/src/include/vsc/dm/IDataTypeBitVector.h`
- New interface path: `src/zuspec/dm/data_type.py::DataTypeBitVector`
- Visitor method name: `visitDataTypeBitVector`
- Context factory name: `mkDataTypeBitVector(width: int) -> DataTypeBitVector`
---

### Mapping: IDataTypeStruct

- Original header path: `packages/vsc-dm/src/include/vsc/dm/IDataTypeStruct.h`
- New interface path: `src/zuspec/dm/data_type.py::DataTypeStruct`
- Visitor method name: `visitDataTypeStruct`
- Context factory name: `mkDataTypeStruct(fields: list[str]) -> DataTypeStruct`
---

### Mapping: ITypeExpr

- Original header path: `packages/vsc-dm/src/include/vsc/dm/ITypeExpr.h`
- New interface path: `src/zuspec/dm/data_type.py::DataTypeExpr`
- Visitor method name: `visitDataTypeExpr`
- Context factory name: `mkDataTypeExpr(expr_type: str) -> DataTypeExpr`
---

### Mapping: IDataTypeArray

- Original header path: `packages/vsc-dm/src/include/vsc/dm/IDataTypeArray.h`
- New interface path: `src/zuspec/dm/data_type.py::DataTypeArray`
- Visitor method name: `visitDataTypeArray`
- Context factory name: `mkDataTypeArray(element_type: str) -> DataTypeArray`
---

### Mapping: IDataTypeBool

- Original header path: `packages/vsc-dm/src/include/vsc/dm/IDataTypeBool.h`
- New interface path: `src/zuspec/dm/data_type.py::DataTypeBool`
- Visitor method name: `visitDataTypeBool`
- Context factory name: `mkDataTypeBool(value: bool) -> DataTypeBool`
---

### Mapping: IDataTypeEnum

- Original header path: `packages/vsc-dm/src/include/vsc/dm/IDataTypeEnum.h`
- New interface path: `src/zuspec/dm/data_type.py::DataTypeEnum`
- Visitor method name: `visitDataTypeEnum`
- Context factory name: `mkDataTypeEnum(enum_type: str) -> DataTypeEnum`
---

### Mapping: IDataTypeList

- Original header path: `packages/vsc-dm/src/include/vsc/dm/IDataTypeList.h`
- New interface path: `src/zuspec/dm/data_type.py::DataTypeList`
- Visitor method name: `visitDataTypeList`
- Context factory name: `mkDataTypeList(element_type: str) -> DataTypeList`
---

### Mapping: IDataTypePtr

- Original header path: `packages/vsc-dm/src/include/vsc/dm/IDataTypePtr.h`
- New interface path: `src/zuspec/dm/data_type.py::DataTypePtr`
- Visitor method name: `visitDataTypePtr`
- Context factory name: `mkDataTypePtr(ref_type: str) -> DataTypePtr`
---

### Mapping: IDataTypeRef

- Original header path: `packages/vsc-dm/src/include/vsc/dm/IDataTypeRef.h`
- New interface path: `src/zuspec/dm/data_type.py::DataTypeRef`
- Visitor method name: `visitDataTypeRef`
- Context factory name: `mkDataTypeRef(ref_type: str) -> DataTypeRef`
---

### Mapping: IDataTypeString

- Original header path: `packages/vsc-dm/src/include/vsc/dm/IDataTypeString.h`
- New interface path: `src/zuspec/dm/data_type.py::DataTypeString`
- Visitor method name: `visitDataTypeString`
- Context factory name: `mkDataTypeString(value: str) -> DataTypeString`
---

### Mapping: ITypeConstraintBlock

- Original header path: `packages/vsc-dm/src/include/vsc/dm/ITypeConstraintBlock.h`
- New interface path: `src/zuspec/dm/data_type.py::TypeConstraintBlock`
- Visitor method name: `visitTypeConstraintBlock`
- Context factory name: `mkTypeConstraintBlock(constraints: list[str]) -> TypeConstraintBlock`
---

### Mapping: ITypeConstraintExpr

- Original header path: `packages/vsc-dm/src/include/vsc/dm/ITypeConstraintExpr.h`
- New interface path: `src/zuspec/dm/data_type.py::TypeConstraintExpr`
- Visitor method name: `visitTypeConstraintExpr`
- Context factory name: `mkTypeConstraintExpr(expr: str) -> TypeConstraintExpr`
---

### Mapping: ITypeConstraintIfElse

- Original header path: `packages/vsc-dm/src/include/vsc/dm/ITypeConstraintIfElse.h`
- New interface path: `src/zuspec/dm/data_type.py::TypeConstraintIfElse`
- Visitor method name: `visitTypeConstraintIfElse`
- Context factory name: `mkTypeConstraintIfElse(condition: str, if_true: str, if_false: str) -> TypeConstraintIfElse`
---

### Mapping: ITypeExprBin

- Original header path: `packages/vsc-dm/src/include/vsc/dm/ITypeExprBin.h`
- New interface path: `src/zuspec/dm/data_type.py::TypeExprBin`
- Visitor method name: `visitTypeExprBin`
- Context factory name: `mkTypeExprBin(left: str, right: str, op: str) -> TypeExprBin`
---

### Mapping: ITypeExprRefBottomUp

- Original header path: `packages/vsc-dm/src/include/vsc/dm/ITypeExprRefBottomUp.h`
- New interface path: `src/zuspec/dm/data_type.py::TypeExprRefBottomUp`
- Visitor method name: `visitTypeExprRefBottomUp`
- Context factory name: `mkTypeExprRefBottomUp(ref: str) -> TypeExprRefBottomUp`
---

### Mapping: ITypeExprRefTopDown

- Original header path: `packages/vsc-dm/src/include/vsc/dm/ITypeExprRefTopDown.h`
- New interface path: `src/zuspec/dm/data_type.py::TypeExprRefTopDown`
- Visitor method name: `visitTypeExprRefTopDown`
- Context factory name: `mkTypeExprRefTopDown(ref: str) -> TypeExprRefTopDown`
---

### Mapping: ITypeExprFieldRef

- Original header path: `packages/vsc-dm/src/include/vsc/dm/ITypeExprFieldRef.h`
- New interface path: `src/zuspec/dm/data_type.py::TypeExprFieldRef`
- Visitor method name: `visitTypeExprFieldRef`
- Context factory name: `mkTypeExprFieldRef(field: str) -> TypeExprFieldRef`
---

## 9) Style and CI

- Run formatters/linters.
- Ensure no implementations are constructed directly outside `Context`.
- Keep interfaces free of logic; implementation holds behavior.

---

## Definition of Done (DoD)

- Interface added and exported.
- Visitor method added.
- Implementation added with correct `accept()`.
- Context factory method returns the interface and constructs the impl.
- Unit tests pass.
- Mapping and API signature documented.

---

## Quick Checklist

- [ ] Choose family (vsc/arl) and category
- [ ] Create interface in `src/zuspec/dm/...`
- [ ] Add `visit<Type>` to `visitor.py`
- [ ] Implement class in `src/zuspec/dm/impl/...`
- [ ] Add factory in `Context`
- [ ] Update exports
- [ ] Add tests
- [ ] Record mapping/API here
