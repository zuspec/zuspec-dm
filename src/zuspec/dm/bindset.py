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
import abc
from typing import Optional, Protocol, Iterator
from .expr import TypeExpr
from .loc import Loc

class Bind(Protocol):
    
    @property
    @abc.abstractmethod
    def loc(self) -> Optional[Loc]: ...

    @property
    @abc.abstractmethod
    def lhs(self) -> Optional[TypeExpr]: ...

    @property
    @abc.abstractmethod
    def rhs(self) -> Optional[TypeExpr]: ...

class BindSet(Protocol):

    @property
    @abc.abstractmethod
    def binds(self) -> Iterator[Bind]: ...

    @abc.abstractmethod
    def addBind(self, bind : Bind) -> None: ...

    @abc.abstractmethod
    def numBinds(self) -> int: ...

    @abc.abstractmethod
    def getBind(self, i : int) -> Bind: ...


