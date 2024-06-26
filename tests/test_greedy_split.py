from src.priority_group_stratified_split.group_set import Group, GroupSet
from src.priority_group_stratified_split.greedy_split import GreedySplit

def test_get_split():
    groups = [Group('A', 'A', 20), Group('B', 'A', 30), Group('C', 'A', 50), Group('D', 'A', 10),
                Group('E', 'A', 55), Group('F', 'A', 30), Group('G', 'A', 20)]
    groups = GroupSet(groups)

    greedy_split = GreedySplit()
    total = groups.total_size
    hundred, eighty, twenty, ten1, ten2 = greedy_split.get_split(groups, [100/total, 80/total, 20/total, 10/total, 10/total])

    print(hundred.get_uids())
    print(eighty.get_uids())
    print(twenty.get_uids())
    print(ten1.get_uids())
    print(ten2.get_uids())
    assert hundred.total_size == 85
    assert eighty.total_size == 80
    assert twenty.total_size == 20
    assert ten1.total_size == 10
    assert ten2.total_size == 0