from abc import ABC, abstractmethod
from typing import List

class SchemaMigration(ABC):
    @abstractmethod
    def up(self) -> List[str]:
        pass

    @abstractmethod
    def down(self) -> List[str]:
        pass


    