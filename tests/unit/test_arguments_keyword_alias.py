import zuspec.dm as dm
from zuspec.dm.expr import ExprConstant, ExprCall, Keyword
from zuspec.dm.stmt import Arguments, Arg, Alias


def test_arguments_structure():
    args = Arguments(
        posonlyargs=[Arg(arg="x")],
        args=[Arg(arg="y")],
        vararg=Arg(arg="va"),
        kwonlyargs=[Arg(arg="k1")],
        kw_defaults=[ExprConstant(value=1)],
        kwarg=Arg(arg="kwa"),
        defaults=[ExprConstant(value=0)]
    )
    assert args.posonlyargs[0].arg == "x"
    assert args.kw_defaults[0].value == 1
    assert args.defaults[0].value == 0


def test_keyword_and_alias():
    call = ExprCall(func=ExprConstant(value=0), args=[], keywords=[Keyword(arg="a", value=ExprConstant(value=2))])
    assert isinstance(call.keywords[0], Keyword)
    assert call.keywords[0].arg == "a"
    assert call.keywords[0].value.value == 2

    al = Alias(name="m", asname="mm")
    assert al.name == "m" and al.asname == "mm"
