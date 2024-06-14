from priority_group_stratified_split.group_set import GroupSet 

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
        selected_groups.add(g_uid_indexer[group_uid])
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

    closest_sum = float('inf')
    closest_sum_dist = float('inf')

    for group in group_set:
        for sum_value in list(sums_dict):
            current_sum = sum_value + group.size

            # If current_sum position is not occupied by an uid yet
            if sums_dict.get(current_sum) == None:
                sums_dict[current_sum] = group.uid

                # Calculate all possible sums
                current_sum_dist = abs(current_sum - ideal_size)

                if current_sum_dist < closest_sum_dist:
                    closest_sum = current_sum
                    closest_sum_dist = current_sum_dist

    # Return groups that sizes amout to closest_sum
    return backward(sums_dict, closest_sum, group_set)

def stratified_set(group_set:GroupSet, p) -> GroupSet:
    """
        Parameters:
            group_set: A set of groups to get splited
            p: proportion of number of samples in this set split over all samples

        Returns:
            A set of groups splited by classes in a stratified maner with 
            samples amounting to a value as close as possible to [size]
    """
    new_set = GroupSet()
    g_label_indexer = group_set.get_label_indexer()

    for l_group_set in g_label_indexer.values():
        ideal_size = round(l_group_set.total_size * p)

        new_group_set = best_size_groups(l_group_set, ideal_size)
        new_set = new_set | new_group_set
    return new_set

def get_split(group_set:GroupSet, percentages:list[float]) -> list[set[int]]:
    """
        Parameters:
            group_set: GroupSet containing all Groups in the dataset
            percentages: split percentages, e.g., [0.8,0.1,0.1] for a 
                80:10:10 tain, eval, test split
    """
    total_size = group_set.total_size

    if sum(percentages) != 1:
        raise ValueError('percentages should sum to 1')

    # Get percentages indexes
    # e.g., 80:10:10 split it would be [0,1,2]
    ps_idx = [i for i in range(len(percentages))]

    # Order ps_idx from smaller to greater percentages
    # e.g., 80:10:10 split it would be [1,2,0]
    ps_idx.sort(key=lambda idx: percentages[idx])

    # Now we sort percentagens, and ps_idx is how
    # we go back to percentages original order
    # e.g., 10:10:80 and [1,2,0] tells us that 
    # 80 belongs to position 0
    percentages.sort()

    sizes = [round(p*total_size) for p in percentages]
    # Bigger group is what is left from the others
    sizes[-1] = total_size - sum(sizes[:-1])

    sets = [None for _ in range(len(sizes))]

    # Loop trhough sizes, leaving the bigger group out
    for idx, size in zip(ps_idx[:-1], sizes[:-1]):
        new_set = stratified_set(group_set, size/total_size)
        sets[idx] = new_set
        group_set -= new_set

    # The bigger group will be equal to what is left from gourp_set
    sets[ps_idx[-1]] = group_set

    return sets