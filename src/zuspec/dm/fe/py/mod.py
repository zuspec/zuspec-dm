import dataclasses as dc
from typing import List
from ...stmt import Module as _Module, TypeIgnore as _TypeIgnore

# Re-expose to fe.py namespace to match plan
Module = _Module
TypeIgnore = _TypeIgnore
