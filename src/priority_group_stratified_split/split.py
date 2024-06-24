from abc import ABC, abstractmethod
from priority_group_stratified_split.group_set import GroupSet

class Split(ABC):
    @abstractmethod
    def get_split(self, group_set:GroupSet, percentages:list[float]) -> list[GroupSet]:
        pass