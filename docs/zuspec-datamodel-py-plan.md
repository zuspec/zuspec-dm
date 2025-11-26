# Plan: Python AST Datamodel in zuspec.dm.fe.py

Date: 2025-11-26

Goal
- Define a full set of dataclasses that mirror CPython ast nodes and fields, placed under src/zuspec/dm/fe/py, following the dataclass style and Base/Visitor integration used in src/zuspec/dm/[stmt.py, expr.py].
- Reuse existing enums/classes in zuspec.dm where compatible to keep changes minimal.

Guiding principles
- One dataclass per AST node, inheriting zuspec.dm.base.Base.
- Field names and shapes match https://docs.python.org/3/library/ast.html for Python 3.12+, adapted to our Stmt*/Expr* naming convention used in stmt.py/expr.py.
- Use typing Optional and List; default_factory for list fields; kw_only=True dataclasses.
- Keep enums (BinOp, UnaryOp, BoolOp, CmpOp, AugOp) unified with zuspec.dm.expr when possible.
- Do not change existing behavior; new code is additive and isolated under fe/py.

Package layout (new)
- src/zuspec/dm/fe/py/__init__.py: re-export key node types for convenient import.
- src/zuspec/dm/fe/py/mod.py: Module, TypeIgnore.
- src/zuspec/dm/fe/py/stmt.py: statement nodes (FunctionDef, ClassDef, If, For, While, Try, With, Match, etc.).
- src/zuspec/dm/fe/py/expr.py: expression nodes and helpers (Name, Constant, Attribute, Call, containers, comprehensions, f-strings, NamedExpr, etc.).
- src/zuspec/dm/fe/py/args.py: Arguments, Arg, Keyword, Comprehension, WithItem, ExceptHandler, Alias.
- src/zuspec/dm/fe/py/pattern.py: Match, MatchCase and pattern node family (Python 3.10+).
- (Option) src/zuspec/dm/fe/py/imports.py: Import and ImportFrom if preferred split; otherwise in stmt.py.

Naming and mapping
- Follow existing Zuspec conventions: StmtX for statements, ExprX for expressions; keep helper names as in current repo (Keyword, Alias, Arguments, Arg).
- Map CPython ast -> Zuspec name:
  - ast.Module -> Module
  - ast.TypeIgnore -> TypeIgnore
  - ast.Assign -> StmtAssign
  - ast.AugAssign -> StmtAugAssign
  - ast.AnnAssign -> StmtAnnAssign
  - ast.Return -> StmtReturn; ast.Expr -> StmtExpr
  - ast.If -> StmtIf; ast.For/AsyncFor -> StmtFor/StmtAsyncFor; ast.While -> StmtWhile
  - ast.With/AsyncWith -> StmtWith/StmtAsyncWith; ast.Try -> StmtTry; ast.Raise -> StmtRaise; ast.Assert -> StmtAssert
  - ast.FunctionDef/AsyncFunctionDef -> StmtFunctionDef/StmtAsyncFunctionDef
  - ast.ClassDef -> StmtClassDef
  - ast.Import -> StmtImport; ast.ImportFrom -> StmtImportFrom
  - ast.Global -> StmtGlobal; ast.Nonlocal -> StmtNonlocal; ast.Pass/Break/Continue -> StmtPass/StmtBreak/StmtContinue
  - ast.Match/MatchCase -> StmtMatch/StmtMatchCase; patterns under pattern.py (Pattern*, per CPython)
  - ast.BoolOp -> ExprBool (reuse); ast.BinOp -> ExprBin (reuse); ast.UnaryOp -> ExprUnary (reuse enums)
  - ast.Compare -> ExprCompare (reuse CmpOp)
  - ast.Call -> ExprCall (reuse Keyword)
  - ast.Attribute -> ExprAttribute; ast.Subscript -> ExprSubscript + ExprSlice (reuse)
  - ast.Name -> ExprName (new); ast.Starred -> ExprStarred (new)
  - ast.Constant -> ExprConstant (reuse)
  - ast.List/Tuple/Set/Dict -> ExprList/ExprTuple/ExprSet/ExprDict (new)
  - ast.Lambda -> ExprLambda (new); ast.IfExp -> ExprIfExp (new); ast.NamedExpr -> ExprNamedExpr (new)
  - ast.ListComp/SetComp/DictComp/GeneratorExp -> ExprListComp/ExprSetComp/ExprDictComp/ExprGeneratorExp (new)
  - ast.FormattedValue/JoinedStr -> ExprFormattedValue/ExprJoinedStr (new)
  - ast.Await/Yield/YieldFrom -> ExprAwait/StmtYield/ExprYieldFrom (StmtYield mirrors Python where Yield is an expr wrapped in a statement context; we'll provide ExprYield/ExprYieldFrom and use StmtExpr when needed)

Node set and fields (by file)
- mod.py
  - Module(body: List[Stmt], type_ignores: List[TypeIgnore])
  - TypeIgnore(lineno: int, tag: str)
- args.py
  - Arg(arg: str, annotation: Optional[Expr])
  - Arguments(posonlyargs: List[Arg], args: List[Arg], vararg: Optional[Arg], kwonlyargs: List[Arg], kw_defaults: List[Optional[Expr]], kwarg: Optional[Arg], defaults: List[Expr])
  - Keyword(arg: Optional[str], value: Expr)  [reuse zuspec.dm.expr.Keyword if practical]
  - Alias(name: str, asname: Optional[str])
  - Comprehension(target: Expr, iter: Expr, ifs: List[Expr], is_async: bool)
  - WithItem(context_expr: Expr, optional_vars: Optional[Expr])
  - ExceptHandler(type: Optional[Expr], name: Optional[str], body: List[Stmt])
- stmt.py
  - Stmt(Base) base
  - StmtExpr(expr: Expr)
  - StmtAssign(targets: List[Expr], value: Expr)
  - StmtAnnAssign(target: Expr, annotation: Expr, value: Optional[Expr], simple: int)
  - StmtAugAssign(target: Expr, op: AugOp, value: Expr)
  - StmtReturn(value: Optional[Expr])
  - StmtDelete(targets: List[Expr])
  - StmtIf(test: Expr, body: List[Stmt], orelse: List[Stmt])
  - StmtFor(target: Expr, iter: Expr, body: List[Stmt], orelse: List[Stmt])
  - StmtAsyncFor(target: Expr, iter: Expr, body: List[Stmt], orelse: List[Stmt])
  - StmtWhile(test: Expr, body: List[Stmt], orelse: List[Stmt])
  - StmtWith(items: List[WithItem], body: List[Stmt])
  - StmtAsyncWith(items: List[WithItem], body: List[Stmt])
  - StmtTry(body: List[Stmt], handlers: List[ExceptHandler], orelse: List[Stmt], finalbody: List[Stmt])
  - StmtRaise(exc: Optional[Expr], cause: Optional[Expr])
  - StmtAssert(test: Expr, msg: Optional[Expr])
  - StmtImport(names: List[Alias])
  - StmtImportFrom(module: Optional[str], names: List[Alias], level: int)
  - StmtGlobal(names: List[str])
  - StmtNonlocal(names: List[str])
  - StmtFunctionDef(name: str, args: Arguments, body: List[Stmt], decorator_list: List[Expr], returns: Optional[Expr], type_comment: Optional[str])
  - StmtAsyncFunctionDef(name: str, args: Arguments, body: List[Stmt], decorator_list: List[Expr], returns: Optional[Expr], type_comment: Optional[str])
  - StmtClassDef(name: str, bases: List[Expr], keywords: List[Keyword], body: List[Stmt], decorator_list: List[Expr])
  - StmtPass(), StmtBreak(), StmtContinue()
  - StmtMatch(subject: Expr, cases: List[StmtMatchCase]) [pattern.py]
- expr.py
  - Expr(Base) base
  - Reuse enums from zuspec.dm.expr: BinOp, UnaryOp, BoolOp, CmpOp, AugOp; add ExprContext(Load, Store, Del)
  - ExprBin(lhs: Expr, op: BinOp, rhs: Expr) [reuse existing]
  - ExprUnary(op: UnaryOp, operand: Expr) [reuse existing]
  - ExprBool(op: BoolOp, values: List[Expr]) [reuse existing]
  - ExprCompare(left: Expr, ops: List[CmpOp], comparators: List[Expr]) [reuse existing]
  - ExprConstant(value: object, kind: Optional[str]) [reuse existing]
  - ExprName(id: str, ctx: ExprContext)
  - ExprAttribute(value: Expr, attr: str) [reuse existing]
  - ExprSlice(lower: Optional[Expr], upper: Optional[Expr], step: Optional[Expr]) [reuse existing]
  - ExprSubscript(value: Expr, slice: ExprSlice)
  - ExprCall(func: Expr, args: List[Expr], keywords: List[Keyword]) [reuse existing]
  - ExprList(elts: List[Expr], ctx: ExprContext)
  - ExprTuple(elts: List[Expr], ctx: ExprContext)
  - ExprSet(elts: List[Expr])
  - ExprDict(keys: List[Optional[Expr]], values: List[Expr])
  - ExprLambda(args: Arguments, body: Expr)
  - ExprIfExp(test: Expr, body: Expr, orelse: Expr)
  - ExprNamedExpr(target: Expr, value: Expr)
  - ExprListComp(elt: Expr, generators: List[Comprehension])
  - ExprSetComp(elt: Expr, generators: List[Comprehension])
  - ExprDictComp(key: Expr, value: Expr, generators: List[Comprehension])
  - ExprGeneratorExp(elt: Expr, generators: List[Comprehension])
  - ExprFormattedValue(value: Expr, conversion: int, format_spec: Optional[Expr])
  - ExprJoinedStr(values: List[Expr])
  - ExprAwait(value: Expr)
  - ExprYield(value: Optional[Expr])
  - ExprYieldFrom(value: Expr)
  - ExprStarred(value: Expr, ctx: ExprContext)
- pattern.py (Python 3.10+)
  - StmtMatch(subject: Expr, cases: List[StmtMatchCase])
  - StmtMatchCase(pattern: Pattern, guard: Optional[Expr], body: List[Stmt])
  - Pattern base + concrete: PatternValue(value: Expr), PatternSingleton(value: object), PatternSequence(patterns: List[Pattern]), PatternMapping(keys: List[Expr], patterns: List[Pattern], rest: Optional[str]), PatternClass(cls: Expr, patterns: List[Pattern], kwd_attrs: List[str], kwd_patterns: List[Pattern]), PatternAs(pattern: Optional[Pattern], name: Optional[str]), PatternOr(patterns: List[Pattern]), PatternStar(name: Optional[str]), PatternWildcard()

Implementation phases
- Phase 1: Module + core statements/expressions
  - Files: mod.py, args.py, stmt.py (core), expr.py (Name/List/Tuple/Dict/Set, IfExp, Lambda, NamedExpr), minimal pattern stubs omitted.
  - Reuse existing Expr*, enums from zuspec.dm.expr when names/fields align; import and re-export to avoid duplication.
  - Add ExprContext enum locally.
- Phase 2: Comprehensions and async/yield
  - Add Comprehension, Expr[List/Set/Dict]Comp, ExprGeneratorExp, ExprAwait/Yield/YieldFrom, Starred; update stmt FunctionDef/Async* where needed.
- Phase 3: With/Try/Except, Imports, AnnAssign, Async variants
  - Add WithItem, ExceptHandler, StmtWith/AsyncWith, StmtTry; Import/ImportFrom; StmtAnnAssign.
- Phase 4: Pattern matching and f-strings
  - pattern.py full set; ExprFormattedValue/ExprJoinedStr.

Compatibility and reuse
- Import Base from zuspec.dm.base; fields and traversal work with existing Visitor.
- Prefer from zuspec.dm.expr import Expr, Keyword, BinOp, UnaryOp, BoolOp, CmpOp, AugOp when identical to avoid duplication.
- If divergence is required (e.g., ExprName vs existing ExprRef*), keep both; adapters can translate between FE Py nodes and internal nodes.

Minimal code templates (follow current dataclass style)
- Example statement:
  @dc.dataclass(kw_only=True)
  class StmtAssign(Stmt):
      targets: List[Expr] = dc.field(default_factory=list)
      value: Expr = dc.field()
- Example expression:
  @dc.dataclass(kw_only=True)
  class ExprName(Expr):
      id: str = dc.field()
      ctx: ExprContext = dc.field()

Tests (summary)
- Construct sample trees for each node family; verify Base.accept traverses lists and optionals; ensure visitor stubs are generated.
- Golden mapping tests: parse Python code with ast.parse, then build equivalent fe.py trees and assert structural parity (shape/field counts and selected values).

Deliverables
- New package src/zuspec/dm/fe/py with modules above and __init__.py aggregator.
- No breaking changes to existing src/zuspec/dm/*.py.
- Documentation: this plan; brief README in fe/py if needed in a later change.

Out-of-scope now
- Code generation or transformation between CPython ast and fe.py; may be added as adapters later.
- Performance optimizations beyond current Visitor.
