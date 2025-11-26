import zuspec.dm as dm
from zuspec.dm.fe import py as fepy

class MatchVisitor(dm.Visitor):
    def __init__(self,pmod=None):
        self.seen = []
    def visitStmtMatch(self,o):
        self.seen.append('Match')
        o.visitDefault(self)
    def visitStmtMatchCase(self,o):
        self.seen.append('Case')
        o.visitDefault(self)
    def visitPatternValue(self,o):
        self.seen.append('PatternValue')
        o.visitDefault(self)
    def visitExprConstant(self,o):
        self.seen.append(('Const', o.value))

def test_pattern_match_traversal():
    case = fepy.StmtMatchCase(pattern=fepy.PatternValue(value=fepy.ExprConstant(value=10)), guard=None, body=[])
    m = fepy.StmtMatch(subject=fepy.ExprConstant(value=1), cases=[case])
    v = MatchVisitor(dm)
    m.accept(v)
    assert 'Match' in v.seen
    assert 'Case' in v.seen
    assert 'PatternValue' in v.seen
    assert ('Const',1) in v.seen and ('Const',10) in v.seen
