import dataclasses as dc
from typing import Optional, List
from ...stmt import Arg as _Arg, Arguments as _Arguments, StmtExceptHandler as _StmtExceptHandler, WithItem as _WithItem
from ...expr import Keyword as _Keyword
from ...stmt import Alias as _Alias
from ...expr_phase2 import Comprehension as _Comprehension

Arg = _Arg
Arguments = _Arguments
Keyword = _Keyword
Alias = _Alias
Comprehension = _Comprehension
WithItem = _WithItem

@dc.dataclass(kw_only=True)
class ExceptHandler(_StmtExceptHandler):
    # Alias class to match fe.py naming
    pass
