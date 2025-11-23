import zuspec.dm as dm
from zuspec.dm import ExprJoinedStr, ExprFormattedValue, ExprConstant

class V(dm.Visitor):
    def __init__(self, pmod=None):
        self.nodes = []
    def visitExprJoinedStr(self,o):
        self.nodes.append('Joined'); o.visitDefault(self)
    def visitExprFormattedValue(self,o):
        self.nodes.append('Fmt'); o.visitDefault(self)
    def visitExprConstant(self,o):
        self.nodes.append('Const')

def test_joined_formatted_traversal():
    js = ExprJoinedStr(values=[
        ExprConstant(value='a'),
        ExprFormattedValue(value=ExprConstant(value=1), conversion=-1, format_spec=None),
        ExprConstant(value='b')
    ])
    v = V(dm)
    js.accept(v)
    assert v.nodes.count('Joined') == 1
    assert v.nodes.count('Fmt') == 1
    # constants: 'a', 1, 'b'
    assert v.nodes.count('Const') == 3
