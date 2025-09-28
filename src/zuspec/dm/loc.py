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
import dataclasses as dc
from typing import Any, Optional
from .accept import Accept

@dc.dataclass
class Loc(object):
    file : Optional[str] = dc.field(default=None)
    line : int = dc.field(default=-1)
    pos : int = dc.field(default=-1)
    ref : Optional[Any] = dc.field(default=None)

class Locatable(Accept):

    @property
    @abc.abstractmethod
    def loc(self) -> Optional[Loc]: ...
    

