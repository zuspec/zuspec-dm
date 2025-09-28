#****************************************************************************
# Copyright 2019-2025 Matthew Ballance and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#****************************************************************************
import dataclasses as dc
from typing import Iterator, List, Optional
from ..bindset import Bind, BindSet
from ..loc import Loc
from ..expr import TypeExpr

@dc.dataclass
class BindImpl(Bind):
    _loc : Optional[Loc] = dc.field(default=None)
    _lhs : Optional[TypeExpr] = dc.field(default=None)
    _rhs : Optional[TypeExpr] = dc.field(default=None)
    
    @property
    def loc(self) -> Optional[Loc]: 
        return self._loc

    @property
    def lhs(self) -> Optional[TypeExpr]: 
        return self._lhs

    @property
    def rhs(self) -> Optional[TypeExpr]:
        return self._rhs

class BindSetImpl(BindSet):
    _binds : List[Bind] = dc.field(default_factory=list)

    @property
    def binds(self) -> Iterator[Bind]:
        return self._binds.__iter__()

    def addBind(self, bind : Bind) -> None:
        self._binds.append(bind)

    def numBinds(self) -> int:
        return len(self._binds)

    def getBind(self, i : int) -> Bind:
        return self._binds[i]


