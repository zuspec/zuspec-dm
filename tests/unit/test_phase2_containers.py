import zuspec.dm as dm
from zuspec.dm import ExprList, ExprTuple, ExprDict, ExprSet, ExprListComp, ExprDictComp, ExprSetComp, ExprGeneratorExp, Comprehension, ExprIfExp, ExprLambda, ExprNamedExpr
from zuspec.dm import ExprConstant, ExprBin, BinOp, Module, StmtExpr, StmtAssign, StmtReturn, Arguments, Arg

class CollectVisitor(dm.Visitor):
    def __init__(self, pmod=None):
        self.seen = []
    # Provide handlers the test expects to encounter
    def visitExprBin(self,o):
        self.seen.append('Bin'); o.visitDefault(self)
    def visitStmtExpr(self,o):
        self.seen.append('StmtExpr'); o.visitDefault(self)
    def visitArguments(self,o):
        self.seen.append('Arguments'); o.visitDefault(self)
    def visitExprConstant(self,o):
        self.seen.append('Const')
    def visitExprList(self,o):
        self.seen.append('List'); o.visitDefault(self)
    def visitExprTuple(self,o):
        self.seen.append('Tuple'); o.visitDefault(self)
    def visitExprDict(self,o):
        self.seen.append('Dict'); o.visitDefault(self)
    def visitExprSet(self,o):
        self.seen.append('Set'); o.visitDefault(self)
    def visitExprListComp(self,o):
        self.seen.append('ListComp'); o.visitDefault(self)
    def visitExprDictComp(self,o):
        self.seen.append('DictComp'); o.visitDefault(self)
    def visitExprSetComp(self,o):
        self.seen.append('SetComp'); o.visitDefault(self)
    def visitExprGeneratorExp(self,o):
        self.seen.append('GenExp'); o.visitDefault(self)
    def visitComprehension(self,o):
        self.seen.append('Comp'); o.visitDefault(self)
    def visitExprIfExp(self,o):
        self.seen.append('IfExp'); o.visitDefault(self)
    def visitExprLambda(self,o):
        self.seen.append('Lambda'); o.visitDefault(self)
    def visitExprNamedExpr(self,o):
        self.seen.append('NamedExpr'); o.visitDefault(self)
    def visitModule(self,o):
        self.seen.append('Module'); o.visitDefault(self)
    def visitArg(self,o):
        self.seen.append('Arg'); o.visitDefault(self)
    def visitStmtAssign(self,o):
        self.seen.append('StmtAssign'); o.visitDefault(self)
    def visitStmtReturn(self,o):
        self.seen.append('StmtReturn'); o.visitDefault(self)

def test_container_traversal():
    lst = ExprList(elts=[ExprConstant(value=i) for i in range(3)])
    tup = ExprTuple(elts=[ExprConstant(value=i) for i in range(2)])
    dct = ExprDict(keys=[ExprConstant(value='a'), None], values=[ExprConstant(value=1), ExprConstant(value=2)])
    st = ExprSet(elts=[ExprConstant(value=5), ExprConstant(value=6)])
    v = CollectVisitor(dm)
    for node in [lst, tup, dct, st]:
        node.accept(v)
    assert set(['List','Tuple','Dict','Set']).issubset(set(v.seen))
    # Ensure constants traversed
    assert v.seen.count('Const') >= 7

def test_comprehension_traversal():
    comp = Comprehension(target=ExprConstant(value='x'), iter=ExprList(elts=[ExprConstant(value=1), ExprConstant(value=2)]), ifs=[ExprBin(lhs=ExprConstant(value=1), op=BinOp.Add, rhs=ExprConstant(value=2))])
    lc = ExprListComp(elt=ExprConstant(value='y'), generators=[comp])
    dc = ExprDictComp(key=ExprConstant(value='k'), value=ExprConstant(value='v'), generators=[comp])
    sc = ExprSetComp(elt=ExprConstant(value='z'), generators=[comp])
    ge = ExprGeneratorExp(elt=ExprConstant(value='g'), generators=[comp])
    v = CollectVisitor(dm)
    for node in [lc, dc, sc, ge]:
        node.accept(v)
    assert v.seen.count('Comp') == 4
    assert set(['ListComp','DictComp','SetComp','GenExp']).issubset(set(v.seen))

def test_special_exprs():
    ifexp = ExprIfExp(test=ExprConstant(value=True), body=ExprConstant(value='a'), orelse=ExprConstant(value='b'))
    lam = ExprLambda(args=Arguments(args=[Arg(arg='x')]), body=ExprConstant(value=10))
    named = ExprNamedExpr(target=ExprConstant(value='t'), value=ExprConstant(value='v'))
    v = CollectVisitor(dm)
    for n in [ifexp, lam, named]:
        n.accept(v)
    assert set(['IfExp','Lambda','NamedExpr']).issubset(set(v.seen))

def test_module_traversal():
    m = Module(body=[
        StmtExpr(expr=ExprConstant(value=1)),
        StmtAssign(targets=[ExprConstant(value='x')], value=ExprConstant(value=2)),
        StmtReturn(value=ExprConstant(value=3))
    ])
    v = CollectVisitor(dm)
    m.accept(v)
    assert 'Module' in v.seen
    # 1 const per stmt + assign target + return value
    # Expect 4 constants: expr(1), assign target('x'), assign value(2), return value(3)
    assert v.seen.count('Const') == 4
