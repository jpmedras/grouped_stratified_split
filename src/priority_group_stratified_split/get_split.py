import sys
sys.path.append('./src/priority_group_stratified_split')

from group_set import GroupSet

def backward(sum_dict:dict[int:int], best_sum:int, groups:GroupSet) -> GroupSet:
    """
        sum_dict is a dict of type {
            POSSIBLE_SUM: GROUP_UID
        }
        best_sum: best possible sum
    """
    g_uid_indexer = groups.get_uid_indexer()

    selected_groups = GroupSet()

    while best_sum > 0:
        group_uid = sum_dict[best_sum]
        selected_groups.add(group_uid)
        best_sum -= g_uid_indexer[group_uid].size

    return selected_groups 