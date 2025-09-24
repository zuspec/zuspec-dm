
import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .visitor import Visitor

class Accept(abc.ABC):
    @abc.abstractmethod
    def accept(self, v : 'Visitor') -> None: ...

