from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.data_type import DataTypePtr

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitDataTypePtr(self, obj: DataTypePtr):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkDataTypePtr("MyType")
    assert isinstance(t, DataTypePtr)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
