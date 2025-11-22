from __future__ import annotations

def test_smoke():
    import zuspec.dm as dm

    @dm.visitor_dataclass(dm)
    class MyVisitor(dm.Visitor):

        def __post_init__(self):
            print("MyVisitor.post_init")

        def visitBase(self, o : dm.Base):
            print("MyVisitor.visitBase")
            pass
        pass

    @dm.visitor_dataclass(dm)
    class MyVisitor2(MyVisitor):

        def visitComponent(self, o : dm.Component):
            print("MyVisitor2.visitComponent")
            self.visitBase(o)

    v = MyVisitor()
    v2 = MyVisitor2()

    c = dm.Component()
    c.accept(v)
    c.accept(v2)