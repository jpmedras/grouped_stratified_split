from priority_group_stratified_split.split import Split
from priority_group_stratified_split.group_set import GroupSet

class PrioritySplit(Split):
    def __init__(self) -> None:
        return

    def _backward(self, sums_dict:dict[int:int], closest_sum:int, group_set:GroupSet) -> GroupSet:
        """
        @param: sums_dict is a dict of type {
                POSSIBLE_SUM: GROUP_UID
            }
        @param closest_sum: best possible sum
        
        @returns: A GroupSet of groups that sizes amount to [closest_sum]
        """
        g_uid_indexer = group_set.get_uid_indexer()

        selected_groups = GroupSet()

        while closest_sum > 0:
            group_uid = sums_dict[closest_sum]
            selected_groups.add(g_uid_indexer[group_uid])
            closest_sum -= g_uid_indexer[group_uid].size

        return selected_groups 

    def _best_group_set(self, group_set: GroupSet, ideal_size) -> GroupSet:
        """
        @param group_set: A GroupSet from where the sums of group sizes will be calculated
        @param ideal_size: Target size for sum of group sizes

        @returns: The best GroupSet of groups that sizes amount to a value as close to [ideal_size]
            as possible
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

                    # Calculate distance to ideal_size
                    current_sum_dist = abs(current_sum - ideal_size)

                    if current_sum_dist < closest_sum_dist:
                        closest_sum = current_sum
                        closest_sum_dist = current_sum_dist

        # Return groups that sizes amout to closest_sum
        return self._backward(sums_dict, closest_sum, group_set)

    def _stratified_set(self, group_set:GroupSet, p) -> GroupSet:
        """
        @param group_set: A set of groups to get splited
        @param p: proportion of number of samples in this split set over all samples

        @returns: A set of groups splited by classes in a stratified maner with 
            samples amounting to a value as close as possible to
            group_set.total_size * p
        """
        new_set = GroupSet()
        g_label_indexer = group_set.get_label_indexer()

        for l_group_set in g_label_indexer.values():
            ideal_size = round(l_group_set.total_size * p)

            new_group_set = self._best_group_set(l_group_set, ideal_size)
            new_set = new_set | new_group_set
        return new_set

    def get_split(self, group_set:GroupSet, percentages:list[float], tolerance:float=0.05) -> list[GroupSet]:
        """
        @param group_set: GroupSet containing all Groups in the dataset
        @param percentages: split percentages, e.g., [0.8,0.1,0.1] for a 
                80:10:10 tain, eval, test split
        @param tolerance: how much the sum of percentages can deviate from 1

        @return: list of GroupSets with size equal to the @param percentages.
            Each index i is the split set that corresponds to the percentage
            defined in percentages[i]
        """

        if abs(sum(percentages) - 1) > tolerance:
            raise ValueError('percentages should sum to 1 + or - tolerance')

        total_size = group_set.total_size

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

        # Sort group_set to prioretize bigger sets, so that 
        # smaller ones are left to facilitate the subset sum 
        # of the next split set
        group_set.sort(reverse=True)

        sizes = [round(p*total_size) for p in percentages]
        # The bigger group is formed by what is left by the others
        sizes[-1] = total_size - sum(sizes[:-1])

        sets = [None for _ in range(len(sizes))]

        # Loop through sizes, leaving the bigger group out
        for idx, size in zip(ps_idx[:-1], sizes[:-1]):
            new_set = self._stratified_set(group_set, size/total_size)
            sets[idx] = new_set
            group_set -= new_set

        # The bigger group will be equal to what is left by group_set
        sets[ps_idx[-1]] = group_set

        return sets