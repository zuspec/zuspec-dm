from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.data_type import DataTypeRef

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitDataTypeRef(self, obj: DataTypeRef):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkDataTypeRef("MyType")
    assert isinstance(t, DataTypeRef)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
