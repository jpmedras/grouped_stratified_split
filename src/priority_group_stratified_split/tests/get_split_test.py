import sys
sys.path.append('./src/priority_group_stratified_split')

from group_set import Group, GroupSet
from get_split import backward, best_size_groups, get_split

#################
# Test Backward
#################
print('################# Test Backward #################')
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

selected_groups = backward(sum_dict, 7, groups)
print(selected_groups)

#################
# Test Select Groups
#################
print('\n ################# Test Select Groups #################')

selected_groups = best_size_groups(groups, 10)
print(selected_groups)

selected_groups = best_size_groups(groups, 7)
print(selected_groups)

selected_groups = best_size_groups(groups, 5)
print(selected_groups)

#################
# Test Get Split 
#################
print('\n ################# Test Get Split #################')
groups = [Group(0, 'A', 40), Group(1, 'B', 40), Group(2, 'A', 2), Group(3, 'B', 8), Group(4, 'A', 4), Group(5, 'B', 6)]
groups = GroupSet(groups)
sets = get_split(groups, [0.8, 0.1, 0.1])
print(sets)