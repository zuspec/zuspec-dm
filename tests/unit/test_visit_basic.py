import logging
import zuspec.dm as dm
from zuspec.dm.expr import ExprBin, BinOp, ExprConstant

_log = logging.getLogger("test_visit_basic")

@dm.visitor_dataclass(dm)
class CountingVisitor(dm.Visitor):
    def __init__(self, pmod=None):
        self.count = 0
        super().__init__()

    def visitExprConstant(self, o: ExprConstant, virt : bool=True):
        self.count += 1

    def visitExprBin(self, o: ExprBin, virt : bool=True):
        _log.debug("--> visitExprBin")
        self.count += 1
        o.visitDefault(self, type(self))
        _log.debug("<-- visitExprBin")

def test_bin_visit():
    n1 = ExprConstant(value=1)
    n2 = ExprConstant(value=2)
    expr = ExprBin(lhs=n1, op=BinOp.Add, rhs=n2)
    v = CountingVisitor(dm)
    expr.accept(v)
    assert v.count == 3
