from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.data_type import DataTypeBool

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitDataTypeBool(self, obj: DataTypeBool):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkDataTypeBool(True)
    assert isinstance(t, DataTypeBool)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
