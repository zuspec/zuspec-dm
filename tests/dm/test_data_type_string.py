from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.data_type import DataTypeString

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitDataTypeString(self, obj: DataTypeString):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkDataTypeString("hello")
    assert isinstance(t, DataTypeString)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
