import zuspec.dm as dm
from zuspec.dm.expr import ExprConstant, ExprUnary, UnaryOp, ExprBool, BoolOp, ExprCompare, CmpOp, ExprAttribute, ExprSlice, ExprSubscript, ExprCall, ExprBin, BinOp

def test_core_nodes():
    c1 = ExprConstant(value=10)
    c2 = ExprConstant(value=20)
    un = ExprUnary(op=UnaryOp.UAdd, operand=c1)
    bl = ExprBool(op=BoolOp.And, values=[c1, c2])
    cmp = ExprCompare(left=c1, ops=[CmpOp.Lt], comparators=[c2])
    attr = ExprAttribute(value=c1, attr="x")
    sl = ExprSlice(lower=c1, upper=c2, step=None)
    sub = ExprSubscript(value=c1, slice=sl)
    call = ExprCall(func=attr, args=[c1, c2], keywords=[])
    binexpr = ExprBin(lhs=c1, op=BinOp.Add, rhs=c2)
    assert un.operand.value == 10
    assert len(bl.values) == 2
    assert cmp.ops[0] == CmpOp.Lt
    assert attr.attr == "x"
    assert sub.slice is sl
    assert len(call.args) == 2
    assert binexpr.lhs.value == 10
