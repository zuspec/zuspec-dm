import zuspec.dm as dm
from zuspec.dm.fe import py as fepy

class EHVisitor(dm.Visitor):
    def __init__(self,pmod=None):
        self.nodes = []
    def visitExceptHandler(self,o):
        self.nodes.append('ExceptHandler')
        o.visitDefault(self)
    def visitExprConstant(self,o):
        self.nodes.append(('Const', o.value))
    def visitStmtTry(self,o):
        self.nodes.append('Try')
        o.visitDefault(self)

def test_except_handler_alias():
    handler = fepy.ExceptHandler(type=None, name='e', body=[fepy.StmtExpr(expr=fepy.ExprConstant(value=1))])
    trystmt = fepy.StmtTry(body=[], handlers=[handler], orelse=[], finalbody=[])
    v = EHVisitor(dm)
    trystmt.accept(v)
    assert 'Try' in v.nodes
    assert 'ExceptHandler' in v.nodes
    assert ('Const',1) in v.nodes
