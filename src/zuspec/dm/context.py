
import dataclasses as dc
import zuspec.dm as dm
from typing import List, Dict


@dc.dataclass
class Context(object):
    type_m : Dict[str, dm.DataType] = dc.field(default_factory=dict)

