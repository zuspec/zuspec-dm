import zuspec.dm as dm
from zuspec.dm import StmtWith, WithItem, StmtExpr
from zuspec.dm import ExprConstant

class V(dm.Visitor):
    def __init__(self, pmod=None):
        self.nodes = []
    def visitStmtWith(self,o):
        self.nodes.append('With'); o.visitDefault(self)
    def visitWithItem(self,o):
        self.nodes.append('Item'); o.visitDefault(self)
    def visitStmtExpr(self,o):
        self.nodes.append('Expr'); o.visitDefault(self)
    def visitExprConstant(self,o):
        self.nodes.append('Const')

def test_with_multiple_items():
    items = [
        WithItem(context_expr=ExprConstant(value='c1'), optional_vars=ExprConstant(value='as1')),
        WithItem(context_expr=ExprConstant(value='c2'), optional_vars=None)
    ]
    w = StmtWith(items=items, body=[StmtExpr(expr=ExprConstant(value=0))])
    v = V(dm)
    w.accept(v)
    assert v.nodes.count('With') == 1
    assert v.nodes.count('Item') == 2
    # constants: c1, as1, c2, body 0
    assert v.nodes.count('Const') == 4
