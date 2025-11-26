import zuspec.dm as dm
from zuspec.dm.fe import py as fepy

@dm.visitor_dataclass(dm.fe.py)
class NameVisitor(dm.Visitor):
    def __init__(self, pmod=None):
        self.seen = []
    def visitExprName(self,o):
        self.seen.append(('Name', o.id, o.ctx.name))
    def visitExprConstant(self,o):
        self.seen.append(('Const', o.value))
    def visitExprList(self,o):
        self.seen.append(('List', len(o.elts)))
        o.visitDefault(self)

def test_expr_name_traversal():
    n1 = fepy.ExprName(id='x', ctx=fepy.ExprContext.Load)
    n2 = fepy.ExprName(id='y', ctx=fepy.ExprContext.Store)
    lst = fepy.ExprList(elts=[n1, fepy.ExprConstant(value=1), n2])
    v = NameVisitor(dm)
    lst.accept(v)
    assert ('Name','x','Load') in v.seen
    assert ('Name','y','Store') in v.seen
    assert any(e[0]=='Const' and e[1]==1 for e in v.seen)
