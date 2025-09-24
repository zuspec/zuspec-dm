from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.expr import TypeExprFieldRef

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitTypeExprFieldRef(self, obj: TypeExprFieldRef):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkTypeExprFieldRef("field")
    assert isinstance(t, TypeExprFieldRef)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
