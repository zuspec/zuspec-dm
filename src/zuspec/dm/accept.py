
import abc
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .visitor import Visitor

class Accept(Protocol):
    @abc.abstractmethod
    def accept(self, v : 'Visitor') -> None: ...

