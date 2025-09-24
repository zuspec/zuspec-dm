from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.data_type import DataTypeEnum

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitDataTypeEnum(self, obj: DataTypeEnum):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkDataTypeEnum("MyEnum")
    assert isinstance(t, DataTypeEnum)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called
