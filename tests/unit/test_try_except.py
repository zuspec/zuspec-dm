import zuspec.dm as dm
from zuspec.dm import StmtTry, StmtExceptHandler, StmtExpr, StmtReturn
from zuspec.dm import ExprConstant

class V(dm.Visitor):
    def __init__(self, pmod=None):
        self.nodes = []
    def visitStmtTry(self,o):
        self.nodes.append('Try'); o.visitDefault(self)
    def visitStmtExceptHandler(self,o):
        self.nodes.append('Except'); o.visitDefault(self)
    def visitStmtReturn(self,o):
        self.nodes.append('Return'); o.visitDefault(self)
    def visitStmtExpr(self,o):
        self.nodes.append('Expr'); o.visitDefault(self)
    def visitExprConstant(self,o):
        self.nodes.append('Const')

def test_try_except_else_finally_traversal():
    h1 = StmtExceptHandler(type=ExprConstant(value=ValueError.__name__), name='e', body=[StmtExpr(expr=ExprConstant(value=11))])
    h2 = StmtExceptHandler(type=None, name=None, body=[StmtReturn(value=ExprConstant(value=22))])
    t = StmtTry(
        body=[StmtExpr(expr=ExprConstant(value=1))],
        handlers=[h1, h2],
        orelse=[StmtExpr(expr=ExprConstant(value=2))],
        finalbody=[StmtExpr(expr=ExprConstant(value=3))]
    )
    v = V(dm)
    t.accept(v)
    assert v.nodes.count('Try') == 1
    assert v.nodes.count('Except') == 2
    # constants: type(ValueError), 1 in try, 11 in except body, 22 in return, 2 in else, 3 in finally
    assert v.nodes.count('Const') == 6
