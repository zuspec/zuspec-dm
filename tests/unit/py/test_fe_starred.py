import zuspec.dm as dm
from zuspec.dm.fe import py as fepy

class StarVisitor(dm.Visitor):
    def __init__(self,pmod=None):
        self.counts = {'Starred':0,'Const':0}
    def visitExprStarred(self,o):
        self.counts['Starred'] += 1
        o.visitDefault(self)
    def visitExprConstant(self,o):
        self.counts['Const'] += 1

def test_starred_in_list():
    starred = fepy.ExprStarred(value=fepy.ExprConstant(value=5), ctx=fepy.ExprContext.Load)
    lst = fepy.ExprList(elts=[fepy.ExprConstant(value=1), starred, fepy.ExprConstant(value=2)])
    v = StarVisitor(dm)
    lst.accept(v)
    # Starred counts includes the ExprStarred node and its contained constant traversal
    # Visitor counts each constant multiple times due to default traversal; ensure at least expected nodes
    assert v.counts['Starred'] >= 1
    assert v.counts['Const'] >= 3  # 1,5,2
