from typing import Any

class Group:
    def __init__(self, uid:Any, label:str, size:int) -> None:
        """
        An entity that represents a group of samples
        
        @param uid: a unique id for this group
        @param g_class: the class label for the samples in this group
        @param size: number of samples in this group
        """
        self._uid = uid
        self._label = label
        self._size = size

    def __hash__(self) -> int:
        return hash(self._uid)

    def __repr__(self) -> str:
        return f"Group({self._uid}, {self._label}, {self._size})"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def uid(self):
        return self._uid

    @property
    def label(self):
        return self._label

    @property
    def size(self):
        return self._size

class GroupSet:
    """
    Description:
    A set of Group objects

    Parameters:
        groups: A list of Groups
    """
    def __init__(self, groups:list[Group]=None) -> None:
        self._groups = set(groups) if groups else set()
        self._uid_indexer = None
        self._label_indexer = None

        # Init and calc labels and total_size
        self._labels = set()
        self._total_size = 0

        if groups:
            for g in groups:
                self._total_size += g.size
                self._labels.add(g.label)


    def __repr__(self) -> str:
        return f"GroupSet({self._groups})" if len(self._groups) > 0 else 'GroupSet()' 

    def __str__(self) -> str:
        return f"GroupSet({self._groups})" if len(self._groups) > 0 else 'GroupSet()' 

    def __len__(self):
        return len(self._groups) if self._groups else 0

    def __iter__(self):
        return iter(self._groups)

    def __or__(self, other) -> 'GroupSet':
        return GroupSet(self._groups | other._groups)

    def __sub__(self, other: 'GroupSet') -> 'GroupSet':
        return GroupSet(self._groups - other._groups)

    def __isub__(self, other: 'GroupSet') -> 'GroupSet':
        self = GroupSet(self._groups - other._groups)
        return self

    def __eq__(self, other: 'GroupSet') -> bool:
        return self._groups == other._groups

    @property
    def total_size(self) -> int:
        return self._total_size

    @property
    def labels(self) -> set[str]:
        return self._labels

    def add(self, group:Group):
        self._groups.add(group)
        self._total_size += group.size

    def get_uid_indexer(self) -> dict[Any: Group]:
        if self._uid_indexer is None:
            self._uid_indexer = {
                g.uid: g for g in self._groups
            }

        return self._uid_indexer

    def get_label_indexer(self) -> dict[str: 'Groups']:
        if self._label_indexer is None:
            self._label_indexer = {}

            for g in self._groups:
                if g._label not in self._label_indexer:
                    self._label_indexer[g._label] = GroupSet()

                self._label_indexer[g._label].add(g)

        return self._label_indexer

    def get_uids(self) -> list[Any]:
        return [g.uid for g in self._groups]