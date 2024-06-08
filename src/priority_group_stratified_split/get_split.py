import sys
sys.path.append('./src/priority_group_stratified_split')

from group_set import Group, GroupSet

def backward(sums_dict:dict[int:int], closest_sum:int, group_set:GroupSet) -> GroupSet:
    """
    Parameters:
        sums_dict is a dict of type {
            POSSIBLE_SUM: GROUP_UID
        }
        closest_sum: best possible sum
    
    Returns:
        A GroupSet of groups that sizes amount to [closest_sum]
    """
    g_uid_indexer = group_set.get_uid_indexer()

    selected_groups = GroupSet()

    while closest_sum > 0:
        group_uid = sums_dict[closest_sum]
        selected_groups.add(group_uid)
        closest_sum -= g_uid_indexer[group_uid].size

    return selected_groups 

def best_size_groups(group_set: GroupSet, ideal_size) -> GroupSet:
    """
        Parameters:
            group_set: A GroupSet from where the sums of group sizes will be calculated
            ideal_size: Target size for sum of group sizes

        Returns:
            The best GroupSet of groups that sizes amount to a value as close to [ideal_size] as possible
    """
    sums_dict:dict[int:int] = {
        0: -1
    }

    last_sum = 0

    for group in group_set:
        for sum_value in list(sums_dict):
            current_sum = sum_value + group.size

            # If current_sum position is not occupied by an uid yet
            if sums_dict.get(current_sum) == None:
                sums_dict[current_sum] = group.uid

            if current_sum >= ideal_size:
                # Get sum that is colser to ideal_sum
                current_sum_dist = abs(current_sum - ideal_size)
                last_sum_dist = abs(last_sum - ideal_size)

                if current_sum_dist < last_sum_dist:
                    closest_sum = current_sum
                else:
                    closest_sum = last_sum

                # Return groups that sizes amout to closest_sum
                return backward(sums_dict, closest_sum, group_set)
            else:
                last_sum = current_sum

    return GroupSet()