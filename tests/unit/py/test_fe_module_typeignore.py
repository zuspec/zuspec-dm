import zuspec.dm as dm
from zuspec.dm.fe import py as fepy

class ModuleVisitor(dm.Visitor):
    def __init__(self,pmod=None):
        self.ti = 0
        self.const = 0
    def visitModule(self,o):
        o.visitDefault(self)
    def visitTypeIgnore(self,o):
        self.ti += 1
    def visitExprConstant(self,o):
        self.const += 1
    def visitStmtExpr(self,o):
        o.visitDefault(self)

def test_module_typeignore():
    ti = fepy.TypeIgnore(lineno=1, tag='ignore')
    m = fepy.Module(body=[fepy.StmtExpr(expr=fepy.ExprConstant(value=3))], type_ignores=[ti])
    v = ModuleVisitor(dm)
    m.accept(v)
    assert v.ti == 1
    assert v.const == 1
