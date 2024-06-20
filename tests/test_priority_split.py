from src.priority_group_stratified_split.group_set import Group, GroupSet
from src.priority_group_stratified_split.priority_split import PrioritySplit
from itertools import permutations

def test_backward():
    groups = [Group(0, 'C', 2), Group(1, 'A', 3), Group(2, 'A', 5)]
    groups = GroupSet(groups)
    priority_split = PrioritySplit()

    sum_dict = {
        0: None,
        2: 0,
        3: 1,
        5: 1,
        7: 2,
        10: 2
    }

    assert priority_split._backward(sum_dict, 7, groups).get_uids() in [[2,0], [0,2]]
    assert priority_split._backward(sum_dict, 3, groups).get_uids() == [1]
    assert priority_split._backward(sum_dict, 2, groups).get_uids() == [0]

def test_select_groups():
    groups = [Group(0, 'C', 2), Group(1, 'A', 3), Group(2, 'A', 5)]
    groups = GroupSet(groups)
    priority_split = PrioritySplit()

    assert priority_split._best_size_groups(groups, 10).get_uids() in permutations([2,1,0])
    assert priority_split._best_size_groups(groups, 7).get_uids() in permutations([2,0])
    assert priority_split._best_size_groups(groups, 5).get_uids() == [1]

def test_select_groups():
    groups = [Group(0, 'A', 40), Group(1, 'B', 40), Group(2, 'A', 2), Group(3, 'B', 8), Group(4, 'A', 4), Group(5, 'B', 6)]
    groups = GroupSet(groups)
    priority_split = PrioritySplit()

    sets = priority_split.get_split(groups, [0.8, 0.1, 0.1])

    assert sets[0].get_uids() in [[0,1], [1,0]]
    assert sets[1].get_uids() in [[2,3], [3,2], [4,5], [5,4]]
    assert sets[2].get_uids() in [[2,3], [3,2], [4,5], [5,4]]
