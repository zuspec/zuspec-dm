from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.data_type import TypeConstraintExpr

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitTypeConstraintExpr(self, obj: TypeConstraintExpr):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkTypeConstraintExpr("expr")
    assert isinstance(t, TypeConstraintExpr)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
