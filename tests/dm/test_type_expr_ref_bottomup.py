from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.expr import TypeExprRefBottomUp

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitTypeExprRefBottomUp(self, obj: TypeExprRefBottomUp):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkTypeExprRefBottomUp("ref")
    assert isinstance(t, TypeExprRefBottomUp)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
