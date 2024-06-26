from priority_group_stratified_split.split import Split
from priority_group_stratified_split.group_set import GroupSet, Group
from copy import deepcopy

class GreedySplit(Split):
    def __init__(self) -> None:
        return
    def _greedy_group_set(self, group_set: GroupSet, percentages:list[float], remaining_policy:str='w') -> GroupSet:
        # Sort group_set in non inscreasing order
        group_set.sort(reverse=True)

        total_size = group_set.total_size

        ###################################################
        # Using the knapsack problem nomeclature for a more
        # semantic and relatale code
        ####################################################

        capacities = [round(p*total_size) for p in percentages]
        # The bigger group is formed by what is left by the others
        capacities[0] = total_size - sum(capacities[1:])

        loads = [0 for _ in capacities]

        # one to represent each size in sizes
        knapsacks = [GroupSet() for _ in range(len(capacities))]
        len_knapsacks = len(knapsacks)-1
        current_knapsack = 0 # to loop over the sets variable
        last_fit = 0 # to store the last knapsack where a item fitted

        items = group_set.groups
        current_item = 0
        left_items:list[Group] = []

        # We'll go over all knapsacks
        while current_item < len(items):
            item = items[current_item]

            # If current item fits into the current knapsack
            if item.size <= capacities[current_knapsack] - loads[current_knapsack]:
                #print('item', item, 'fits into', capacities[current_knapsack])
                knapsacks[current_knapsack].add(item)
                loads[current_knapsack] += item.size

                last_fit = current_knapsack
                current_item += 1
                continue

            current_knapsack = (current_knapsack +1) % len_knapsacks

            # If we went through all knapsacks and the item did not fit
            if current_knapsack == last_fit:
                left_items.append(item)
                current_item += 1

        # If there are any items left and want to force them into a knapsack  
        if len(left_items) > 0 and remaining_policy != 'n':

            policy = None
            distance = lambda idx, item: abs(capacities[idx] - (loads[idx] + item.size))

            if remaining_policy == 'w':
                weight = lambda idx: 1 - (capacities[idx]-loads[idx])/capacities[idx]
                policy = lambda idx, item: weight(idx) * distance(idx, item)
            else:
                policy = distance

            for item in left_items:
                # Order knapsacks according to the policy
                knapsacks_idx = [i for i in range(len(knapsacks))]
                knapsacks_idx.sort(key=lambda idx: policy(idx, item))

                # Add item in the first one
                knapsacks[knapsacks_idx[0]].add(item)

            return knapsacks

    def get_split(self, group_set:GroupSet, percentages:list[float], tolerance:float=0.05, remaining_policy:str='w') -> list[GroupSet]:
        """
        @param group_set: GroupSet containing all Groups in the dataset
        @param percentages: split percentages, e.g., [0.8,0.1,0.1] for a 
                80:10:10 tain, eval, test split
        @param tolerance: how much the sum of percentages can deviate from 1
        @param remaining_policy: How to force remaining groups into the split sets:
                'n': None. Remaining items won't be putted into any split set.
                'm': Minimum error. Remaining items will go to split sets causing 
                    minimum deviation from the ideal set size.
                'w': Weighted error. Like Minimum error, but it weights by how empty
                    the split set is. Empty split sets will receive remaining items
                    regardless of the distance to the ideal set size.

        @return: list of GroupSets with size equal to the @param percentages.
            Each index i is the split set that corresponds to the percentage
            defined in percentages[i]
        """

        if abs(sum(percentages) - 1) > tolerance:
            raise ValueError('Percentages should sum to 1 + or - tolerance')
        
        if remaining_policy not in ['n', 'm', 'w']:
                raise ValueError('Invalid Remaining Policy')

        # Get percentages indexes
        # e.g., 70:10:20 split it would be [0,1,2]
        ps_idx = [i for i in range(len(percentages))]

        # Order ps_idx from greater to smaller percentages
        # e.g., 70:20:10 split it would be [0,2,1]
        ps_idx.sort(key=lambda idx: percentages[idx], reverse=True)

        # Now we sort percentagens in non increasing
        # order, and ps_idx is how we go back to
        # to percentages original order
        # e.g., 70:20:10 and [0,2,1] tells us that 
        # 20 belongs to position 2
        percentages.sort(reverse=True)

        knapsacks = [GroupSet() for _ in knapsacks]

        g_label_indexer = group_set.get_label_indexer()

        # Get greedy sets for each label
        for l_group_set in g_label_indexer.values():
            l_knapsacks = self._greedy_group_set(l_group_set, percentages, remaining_policy)

            for idx, l_ks in enumerate(l_knapsacks):
                knapsacks[idx] |= l_ks

        ordered_knapsacks = [None for _ in knapsacks]

        for idx, ks in zip(ps_idx, knapsacks):
            ordered_knapsacks[idx] = ks

        return ordered_knapsacks