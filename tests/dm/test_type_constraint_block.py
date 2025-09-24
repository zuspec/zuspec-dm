from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.data_type import TypeConstraintBlock

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitTypeConstraintBlock(self, obj: TypeConstraintBlock):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkTypeConstraintBlock(["c1", "c2"])
    assert isinstance(t, TypeConstraintBlock)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
