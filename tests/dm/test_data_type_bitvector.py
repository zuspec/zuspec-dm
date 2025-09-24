from zuspec.dm.impl.context import Context
from zuspec.dm.visitor import Visitor
from zuspec.dm.data_type import DataTypeBitVector

class SpyVisitor(Visitor):
    def __init__(self):
        self.called = False
    def visitDataTypeBitVector(self, obj: DataTypeBitVector) -> None:
        self.called = True

def test_factory_and_visit():
    ctx = Context()
    t = ctx.mkDataTypeBitVector(8)
    assert isinstance(t, DataTypeBitVector)
    sv = SpyVisitor()
    t.accept(sv)
    assert sv.called

class SpyVisitorStruct(Visitor):
    def __init__(self):
        self.called = False
    def visitDataTypeStruct(self, obj):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass
    def visitDataTypeExpr(self, obj):
        pass

def test_factory_and_visit_struct():
    ctx = Context()
    t = ctx.mkDataTypeStruct(["f1", "f2"])
    assert hasattr(t, "fields")
    sv = SpyVisitorStruct()
    t.accept(sv)
    assert sv.called

class SpyVisitorExpr(Visitor):
    def __init__(self):
        self.called = False
    def visitDataTypeExpr(self, obj):
        self.called = True
    def visitDataTypeBitVector(self, obj):
        pass
    def visitDataTypeStruct(self, obj):
        pass

def test_factory_and_visit_expr():
    ctx = Context()
    t = ctx.mkDataTypeExpr("binop")
    assert hasattr(t, "expr_type")
    sv = SpyVisitorExpr()
    t.accept(sv)
    assert sv.called
