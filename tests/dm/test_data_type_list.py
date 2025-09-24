from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.data_type import DataTypeList

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitDataTypeList(self, obj: DataTypeList):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkDataTypeList("int")
    assert isinstance(t, DataTypeList)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
