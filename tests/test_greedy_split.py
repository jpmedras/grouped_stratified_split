from src.priority_group_stratified_split.group_set import Group, GroupSet
from src.priority_group_stratified_split.greedy_split import GreedySplit

def test_get_split():
    groups = [Group('A', 'A', 45), Group('B', 'A', 20), Group('C', 'A', 20), Group('D', 'A', 15)]
    groups = GroupSet(groups)

    greedy_split = GreedySplit()

    train, eval, test = greedy_split.get_split(groups, [0.7, 0.1, 0.2])

    print(train.get_uids())
    print(eval.get_uids())
    print(test.get_uids())

    assert train.total_size == 65
    assert eval.total_size == 15
    assert test.total_size == 20