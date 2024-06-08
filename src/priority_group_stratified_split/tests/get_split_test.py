import sys
sys.path.append('./src/priority_group_stratified_split')

from group_set import Group, GroupSet
from get_split import backward

#################
# Test Backward
#################
groups = [Group(0, 'C', 2), Group(1, 'A', 3), Group(2, 'A', 5)]
groups = GroupSet(groups)

sum_dict = {
    0: None,
    2: 0,
    3: 1,
    5: 1,
    7: 2,
    10: 2
}

best_sum = 7

selected_groups = backward(sum_dict, best_sum, groups)
print(selected_groups)