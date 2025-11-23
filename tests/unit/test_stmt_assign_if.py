
import logging
import zuspec.dm as dm
from zuspec.dm.expr import ExprConstant, ExprBin, BinOp
from zuspec.dm.stmt import StmtAssign, StmtIf, StmtExpr

_log = logging.getLogger("test_stmt_assign_if")

class CountingVisitor(dm.Visitor):
    def __init__(self, pmod=None):
        self.nodes = []

    def visitStmtIf(self, o: StmtIf):
        self.nodes.append('If')
        o.visitDefault(self)

    def visitStmtAssign(self, o: StmtAssign):
        _log.debug("visitStmtAssign")
        self.nodes.append('Assign')
        o.visitDefault(self)

    def visitExprBin(self, o: ExprBin):
        self.nodes.append('Bin')
        o.visitDefault(self)

    def visitExprConstant(self, o: ExprConstant):
        self.nodes.append('Const')

def test_if_assign():
    cond = ExprBin(lhs=ExprConstant(value=1), op=BinOp.Add, rhs=ExprConstant(value=2))
    assign = StmtAssign(targets=[ExprConstant(value=0)], value=ExprConstant(value=3))
    ifstmt = StmtIf(test=cond, body=[assign], orelse=[])
    v = CountingVisitor(dm)
    ifstmt.accept(v)
    assert 'If' in v.nodes
    assert 'Assign' in v.nodes
    assert 'Bin' in v.nodes
    assert v.nodes.count('Const') >= 4  # 1,2,0,3
