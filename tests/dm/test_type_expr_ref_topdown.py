from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.expr import TypeExprRefTopDown

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitTypeExprRefTopDown(self, obj: TypeExprRefTopDown):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkTypeExprRefTopDown("ref")
    assert isinstance(t, TypeExprRefTopDown)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
