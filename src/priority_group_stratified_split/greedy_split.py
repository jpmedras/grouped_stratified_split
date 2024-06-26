from priority_group_stratified_split.split import Split
from priority_group_stratified_split.group_set import GroupSet

class GreedySplit(Split):
    def __init__(self) -> None:
        return

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

        # Sort group_set in non inscreasing order
        print()
        print('BEFORE SORT', group_set._groups)
        group_set.sort(reverse=True)
        print('AFTER SORT', group_set._groups)
        print()

        ###################################################
        # Using the knapsack problem nomeclature for a more
        # semantic and relatale code
        ####################################################

        knapsacks_capacities = [round(p*total_size) for p in percentages]
        # The bigger group is formed by what is left by the others
        knapsacks_capacities[-1] = total_size - sum(knapsacks_capacities[:-1])
        print('knapsacks_capacities:', knapsacks_capacities)

        # one to represent each size in sizes
        knapsacks = [GroupSet() for _ in range(len(knapsacks_capacities))]
        len_knapsacks = len(knapsacks)-1
        current_knapsack = 0 # to loop over the sets variable
        last_fit = 0 # to store the last knapsack where a item fitted

        items_dict = group_set.get_uid_indexer()
        items = group_set.get_uids()
        len_items = len(items)
        current_item = 0

        # We'll go over all knapsacks
        while current_item < len_items:
            item = items_dict[items[current_item]]

            # If current item fits into the current knapsack
            if item.size <= knapsacks_capacities[current_knapsack]:
                print('item', item, 'fits into', knapsacks_capacities[current_knapsack])
                knapsacks[current_knapsack].add(item)
                knapsacks_capacities[current_knapsack] -= item.size

                last_fit = current_knapsack
                current_item += 1

                continue

            current_knapsack = (current_knapsack +1) % len_knapsacks

            # If we went through all knapsacks and the item did not fit
            if current_knapsack == last_fit:
                current_item += 1

        # If there are items left
        

        print('knapsacks_capacities END', knapsacks_capacities)
        return knapsacks