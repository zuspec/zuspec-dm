from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.data_type import TypeConstraintIfElse

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitTypeConstraintIfElse(self, obj: TypeConstraintIfElse):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkTypeConstraintIfElse("cond", "true", "false")
    assert isinstance(t, TypeConstraintIfElse)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
