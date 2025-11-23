import zuspec.dm as dm
from zuspec.dm import StmtMatch, StmtMatchCase, PatternValue, PatternAs, PatternOr, StmtExpr
from zuspec.dm import ExprConstant

class V(dm.Visitor):
    def __init__(self, pmod=None):
        self.nodes = []
    def visitStmtMatch(self,o):
        self.nodes.append('Match'); o.visitDefault(self)
    def visitStmtMatchCase(self,o):
        self.nodes.append('Case'); o.visitDefault(self)
    def visitPatternValue(self,o):
        self.nodes.append('PVal'); o.visitDefault(self)
    def visitPatternAs(self,o):
        self.nodes.append('PAs'); o.visitDefault(self)
    def visitPatternOr(self,o):
        self.nodes.append('POr'); o.visitDefault(self)
    def visitStmtExpr(self,o):
        self.nodes.append('Expr'); o.visitDefault(self)
    def visitExprConstant(self,o):
        self.nodes.append('Const')

def test_match_traversal():
    cases = [
        StmtMatchCase(pattern=PatternValue(value=ExprConstant(value=1)), guard=None, body=[StmtExpr(expr=ExprConstant(value='one'))]),
        StmtMatchCase(pattern=PatternOr(patterns=[PatternValue(value=ExprConstant(value=2)), PatternValue(value=ExprConstant(value=3))]), guard=None, body=[StmtExpr(expr=ExprConstant(value='two-three'))]),
        StmtMatchCase(pattern=PatternAs(pattern=None, name='x'), guard=None, body=[StmtExpr(expr=ExprConstant(value='any'))])
    ]
    m = StmtMatch(subject=ExprConstant(value=1), cases=cases)
    v = V(dm)
    m.accept(v)
    assert v.nodes.count('Match') == 1
    assert v.nodes.count('Case') == 3
    # constants: subject 1, pattern 1, 2, 3, and 3 body strings
    assert v.nodes.count('Const') == 7
