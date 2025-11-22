# Zuspec Data Model Expansion Plan

Date: 2025-11-22

Goal: Extend existing zuspec.dm data model to be a structured superset of the Python AST (https://docs.python.org/3/library/ast.html), while preserving current conventions (dataclasses, BaseP protocol, dynamic Visitor generation, Profiles).

## 1. Guiding Principles
- Every AST element that represents a semantic node is a dataclass implementing BaseP (inherit Base).
- Maintain separation between pure data description (DataType*, Field, Bind) and executable/behavior constructs (Exec*, ExecStmt* hierarchy).
- Provide explicit node types where Python AST collapses variants into enums (eg BinOp, UnaryOp, BoolOp, Compare) for improved clarity.
- Keep loc (Loc) optional per node for source mapping.
- Support future domain-specific constructs (hardware/component concepts) orthogonally to Python core nodes via additional DataType* subclasses.

## 2. Current Coverage Summary
Implemented (as of 2025-11-22):
- Core: Base, Loc; Visitor infrastructure (dynamic per-profile generation)
- DataType: DataTypeInt, DataTypeStruct, DataTypeClass, DataTypeComponent, DataTypeExpr, DataTypeEnum, DataTypeString
- Fields/Binding: Bind, BindSet, Field, FieldInOut
- Enums: BinOp, UnaryOp, BoolOp, CmpOp, AugOp
- Expressions: Expr, ExprBin, ExprConstant, ExprUnary, ExprBool, ExprCompare, ExprAttribute, ExprSlice, ExprSubscript, ExprCall; reference forms (ExprRef, TypeExprRefSelf, ExprRefField, ExprRefPy, ExprRefBottomUp, TypeExprRefTopDown)
- Statements: Stmt, StmtExpr, StmtAssign, StmtAugAssign, StmtReturn, StmtIf, StmtFor, StmtWhile, StmtBreak, StmtContinue, StmtPass, StmtRaise, StmtAssert
- Visitor traversal: Base.visitDefault iterates BaseP fields and lists; Optional[BaseP] fields are traversed when not None

Incomplete / Not yet implemented:
- Module/File: Module, TypeIgnore
- Functions/Classes: StmtFunctionDef, StmtClassDef (bases, keywords, decorators)
- Imports: StmtImport, StmtImportFrom
- Scope control: StmtGlobal, StmtNonlocal
- With/Context Manager: StmtWith, WithItem
- Error handling: StmtTry, StmtExceptHandler, with orelse/finally
- Expression containers and comprehensions: List/Tuple/Dict/Set nodes; ListComp/DictComp/SetComp/GeneratorExp, Comprehension
- Other expressions: ExprLambda, ExprIfExp, ExprNamedExpr; formatted strings (ExprJoinedStr, ExprFormattedValue)
- Pattern matching: Match/MatchCase and pattern nodes
- Domain-specific: StmtExecSync
- Type-model: DataTypeFunction, DataTypeAlias

## 3. Proposed Class Hierarchy Additions
(Names prefixed with Expr* or Stmt* for clarity; still inherit Base.)

### 3.1 Module/File Level
- Module: fields: body: List[Stmt]; type_ignores: List[TypeIgnore]
- TypeIgnore: lineno: int; tag: str

### 3.2 Statement Base
- Stmt(Base): common base for all concrete statements (ExecStmt will be migrated to dataclass forms inheriting Stmt).
- Replace abstract ExecStmt* protocols with dataclass concrete subclasses (align with Python AST naming):
  - StmtExpr(expr: Expr)
  - StmtAssign(targets: List[Expr], value: Expr)
  - StmtAugAssign(target: Expr, op: AugOp enum, value: Expr)
  - StmtReturn(value: Optional[Expr])
  - StmtIf(test: Expr, body: List[Stmt], orelse: List[Stmt])
  - StmtFor(target: Expr, iter: Expr, body: List[Stmt], orelse: List[Stmt])
  - StmtWhile(test: Expr, body: List[Stmt], orelse: List[Stmt])
  - StmtBreak()
  - StmtContinue()
  - StmtPass()
  - StmtRaise(exc: Optional[Expr], cause: Optional[Expr])
  - StmtAssert(test: Expr, msg: Optional[Expr])
  - StmtTry(body: List[Stmt], handlers: List[StmtExceptHandler], orelse: List[Stmt], finalbody: List[Stmt])
  - StmtExceptHandler(type: Optional[Expr], name: Optional[str], body: List[Stmt])
  - StmtWith(items: List[WithItem], body: List[Stmt])
  - WithItem(context_expr: Expr, optional_vars: Optional[Expr])
  - StmtFunctionDef(name: str, args: Arguments, body: List[Stmt], decorator_list: List[Expr], returns: Optional[Expr])
  - StmtClassDef(name: str, bases: List[Expr], keywords: List[Keyword], body: List[Stmt], decorator_list: List[Expr])
  - StmtImport(names: List[Alias])
  - StmtImportFrom(module: Optional[str], names: List[Alias], level: int)
  - StmtGlobal(names: List[str])
  - StmtNonlocal(names: List[str])
  - StmtExecSync(clock: Expr, reset: Expr, body: List[Stmt]) (domain-specific; extends StmtWith semantics)
  - (Later) StmtMatch(subject: Expr, cases: List[StmtMatchCase]) etc.

Support objects:
- Alias(name: str, asname: Optional[str])
- Keyword(arg: Optional[str], value: Expr)
- Arguments(posonlyargs: List[Arg], args: List[Arg], vararg: Optional[Arg], kwonlyargs: List[Arg], kw_defaults: List[Optional[Expr]], kwarg: Optional[Arg], defaults: List[Expr])
- Arg(arg: str, annotation: Optional[Expr])

### 3.3 Expressions
Add enums:
- AugOp (Add, Sub, Mult, Div, Mod, Pow, LShift, RShift, BitAnd, BitOr, BitXor, FloorDiv)
- UnaryOp (Invert, Not, UAdd, USub)
- BoolOp (And, Or)
- CmpOp (Eq, NotEq, Lt, LtE, Gt, GtE, Is, IsNot, In, NotIn)

Add classes:
- ExprUnary(op: UnaryOp, operand: Expr)
- ExprBoolOp(op: BoolOp, values: List[Expr])
- ExprCompare(left: Expr, ops: List[CmpOp], comparators: List[Expr])
- ExprConstant(value: object, kind: Optional[str])
- ExprAttribute(value: Expr, attr: str)
- ExprSubscript(value: Expr, slice: ExprSlice)
- ExprSlice(lower: Optional[Expr], upper: Optional[Expr], step: Optional[Expr])
- ExprList(elts: List[Expr], ctx: ExprContext enum)
- ExprTuple(elts: List[Expr], ctx: ExprContext)
- ExprDict(keys: List[Optional[Expr]], values: List[Expr])
- ExprSet(elts: List[Expr])
- ExprCall(func: Expr, args: List[Expr], keywords: List[Keyword])
- ExprLambda(args: Arguments, body: Expr)
- ExprIfExp(test: Expr, body: Expr, orelse: Expr)
- ExprListComp(elt: Expr, generators: List[Comprehension])
- ExprDictComp(key: Expr, value: Expr, generators: List[Comprehension])
- ExprSetComp(elt: Expr, generators: List[Comprehension])
- ExprGeneratorExp(elt: Expr, generators: List[Comprehension])
- Comprehension(target: Expr, iter: Expr, ifs: List[Expr], is_async: bool)
- ExprJoinedStr(values: List[Expr])
- ExprFormattedValue(value: Expr, conversion: int, format_spec: Optional[Expr])
- ExprNamedExpr(target: Expr, value: Expr)

Context enum:
- ExprContext(Load, Store, Del) for container elements (mirrors ast.Load etc.)

Domain-specific expression additions retained:
- Existing ExprRef* classes integrate as reference forms analogous to ast.Name / ast.Attribute / lexical variable access. Potential alignment: ExprRefPy ~ ast.Name, ExprRefField ~ ast.Attribute, ExprRefBottomUp ~ scope-relative name (non-Python extension).

### 3.4 Integration with DataType Hierarchy
- DataTypeClass / DataTypeStruct correspond loosely to StmtClassDef + Field definitions; maintain separation (DataType* represent declared types; StmtClassDef appears in executable syntax tree).
- Add DataTypeFunction(signature: Arguments, returns: Optional[DataType], body: Optional[List[Stmt]]) bridging function declarations in a type context.
- Add DataTypeAlias(target: DataType) for type aliasing (Python: 'TypeAlias' semantics) later phase.

### 3.5 Visitor Adjustments
- Profile registration will automatically pick up new dataclass nodes if they reside in package namespace.
- Ensure all added classes inherit Base so dynamic visitor generation supplies visit<ClassName> stubs.
- Provide manual visitor overrides for high-frequency nodes (ExprBin, ExprCompare, StmtAssign, StmtIf, StmtFor) where performance optimizations or custom traversal needed.
- Enhance Base.visitDefault to iterate lists (current implementation ignores list fields). Update logic to:
  - If field value is list: iterate; if element is BaseP call accept.
  - Handle Optional BaseP.

(Separate change: refine introspection; outside scope of this document but required for traversal of newly added list-heavy nodes.)

## 4. Phased Implementation Plan (with status as of 2025-11-22)
Phase 1 (Core Statements & Expressions):
- Implement Stmt*, Arguments, Arg, Keyword, Alias
- Implement core Expression classes: Unary, BoolOp, Compare, Constant, Attribute, Subscript, Slice, Call
- Extend Base.visitDefault to support lists & optionals
- Add enums (UnaryOp, BoolOp, CmpOp, AugOp)
Status: Complete. Implemented: core Stmt* (Expr/Assign/AugAssign/Return/If/For/While/Break/Continue/Pass/Raise/Assert), core Expr (Constant/Unary/Bool/Compare/Attribute/Slice/Subscript/Call), enums, list/optional traversal, and support objects (Arguments/Arg/Keyword/Alias).

Phase 2 (Containers & Comprehensions):
- List/Tuple/Dict/Set, ListComp/DictComp/SetComp/GeneratorExp, Comprehension, IfExp, Lambda, NamedExpr
- Module root node
Status: Not started. None of the container/comprehension/module nodes are implemented.

Phase 3 (Control Flow & Error Handling):
- Try/Except/Finally, With, Raise, Assert, Break, Continue, Pass
- For, While (already in Phase 1 if desired, else here)
Status: Partially complete. For/While/Break/Continue/Pass/Raise/Assert implemented; Try/Except/With not implemented.

Phase 4 (Advanced / Python 3.10+):
- Match / MatchCase / pattern nodes
- Formatted strings (JoinedStr, FormattedValue)
Status: Not started.

Phase 5 (Domain-Specific Extensions):
- StmtExecSync concrete
- DataTypeFunction
- DataTypeAlias
Status: Not started.

## 5. Test Plan (tests/unit)
Testing strategy: granular construction + visitor traversal verification + structural integrity validation.

Test Modules (filenames suggested):
1. test_visit_basic.py
   - Build simple ExprBin tree; ensure visitor auto-stubs invoked; verify custom visitor override works.
2. test_expr_core.py
   - Instantiate each Phase 1 expression node (Unary, BoolOp, Compare, Constant, Attribute, Subscript/Slice, Call) and assert field retention and accept traversal counts.
3. test_stmt_assign_if.py
   - Build nested StmtIf with Assign and ExprBin; verify traversal order and list handling.
4. test_arguments_functiondef.py
   - Construct StmtFunctionDef with varied arguments (defaults, annotations); verify defaults length and visitor traversal.
5. test_loop_stmts.py
   - For / While with orelse; ensure orelse visited.
6. test_try_except.py
   - Try with multiple handlers, else, finally; verify all visited.
7. test_with_stmt.py
   - With with multiple items; verify context_expr and optional_vars visited.
8. test_comprehensions.py
   - ListComp, DictComp, GeneratorExp with multiple Comprehension clauses including ifs.
9. test_containers_literals.py
   - List/Tuple/Set/Dict constant nodes; ensure element traversal.
10. test_lambda_namedexpr_ifexp.py
    - Validate specialized expression forms.
11. test_formatted_string.py (Phase 4)
    - JoinedStr + FormattedValue combination.
12. test_module_root.py
    - Module containing diverse body; ensure top-level body traversal.
13. test_execsync_domain.py
    - StmtExecSync visited; confirm clock/reset/body.
14. test_datatype_function.py
    - DataTypeFunction integration; ensure body traversal.

Visitor test approach:
- Implement MinimalCountingVisitor subclass overriding visitBase to increment a counter, customizing a few node-specific visit methods to record type names.
- Use Profile registration to auto-generate visit methods; assert presence via hasattr.

Edge Cases:
- Optional fields None should not raise errors during traversal.
- Empty lists handled gracefully.
- Compare with multiple ops/comparators alignment of lengths.

Performance Smoke Test:
- Build large synthetic tree (e.g., nested loops + lots of assignments) and ensure traversal completes under time threshold (<50ms for ~1000 nodes).

## 6. File Placement
- New node class implementations: src/zuspec/dm/ (may split into expr_nodes.py, stmt_nodes.py for clarity or extend existing expr.py / exec.py carefully keeping minimal diff; initial plan: create new files to avoid large modifications to existing ones.)
- Update profile registration (if not already) in src/zuspec/dm/__init__.py to include new modules.
- Tests in tests/unit/ matching filenames above.

## 7. Minimal Changes Required Initially
For Phase 1 commit:
- Modify Base.visitDefault to support list and Optional.
- Add new enums/classes for core expressions and statements.
- Add simple visitor test to confirm dynamic method creation.

## 8. Risks & Mitigations
- Risk: Dynamic visitor generation relies on introspection; adding many classes may slow startup. Mitigation: Lazy registration or caching; out-of-scope for initial phases.
- Risk: Name collisions between existing ExprRef* and new ExprAttribute/ExprName. Mitigation: Keep existing names; optionally introduce ExprName for simple identifier later.
- Risk: Large PR complexity. Mitigation: Phase commits.

## 9. Open Questions
- Should DataTypeClass automatically create StmtClassDef representation or remain separate? (Current plan: keep separate.)
- Integrate Python typing annotations directly into DataType* vs storing raw Expr? (Future enhancement.)
- Pattern matching support timeline depends on consumer needs.

## 10. Summary
This plan enumerates a phased build-out to achieve a superset of Python AST within the zuspec.dm framework, aligning naming with Python where practical while preserving domain-specific extensions. Unit tests will validate structural integrity, traversal correctness, and visitor dynamic method generation across all new node types.
