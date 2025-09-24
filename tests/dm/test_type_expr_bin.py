from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.expr import TypeExprBin

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitTypeExprBin(self, obj: TypeExprBin):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkTypeExprBin("left", "right", "op")
    assert isinstance(t, TypeExprBin)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
