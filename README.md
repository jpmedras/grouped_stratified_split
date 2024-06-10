# Priority Stratified Group Split
## The Problem
Video classifying can be a challenging task, not only for the construction of the neural model itself, but also for the dataset split into train, validation and test sets. The videos are generally split into smaller slices/segments of a few seconds. Each of these arrays of segments is considered a group. These groups can’t repeat in the split sets, that is, if a group is present in the train set, it can’t have any of its segments also present in the validation or test sets. This work aims to respond to the following question: **How to distribute the groups of different sizes between the split sets balanced by its classes?**

More specifically, this work will deal with the split of the [NES-MVDB](https://github.com/rubensolv/NES-VMDB) dataset. It contains gameplay videos of all the Nintendo Entertainment System (NES) games. We want to classify these videos by genre. The dataset contain the two following tables:

<img src="https://github.com/jpmedras/priority_group_stratified_split/blob/main/assets/imgs/slices_table.png" width="720px" align="center" alt="Slices Table">

<img src="https://github.com/jpmedras/priority_group_stratified_split/blob/main/assets/imgs/genres_table.png" align="center" alt="Genres Table">

<br>

Since we’ve got 95.899 segments, an 80:10:10 split would ideally have 9.590 segments for validation, that same amount for test, and 76.719 for train. Another way of doing that would be to perform an 80:10:10 split for each game genre, that is, a stratified split, that would guarantee that the sets are balanced by genre. Again, the problem is that each group of gameplay segments can’t overlap each other inside the split sets.

The Scikit Learn library already contains a [StratifiedGroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedGroupKFold.html#stratifiedgroupkfold) function, which performs the split of the non overlapping groups into K folds of the same size in a stratified manner, but it doesn't have a similar method of performing a classic train, validation, test split.

## The Solution
This problem can be seen as a [subset sum](https://en.wikipedia.org/wiki/Subset_sum_problem) execution for each slipt set and class. In our case, for each split set, a subset sum can be performed to get the gameplays that will enter them, with amount of slices proportional to each of the classes. The sums will be performed over the number of slices/segments each gameplay contains, and the set of groups that amount to a value closer to the target will be selected. 

### Example:
If our dataset contains the following groups: 
<br><br>
Group(0, 'A', 40), Group(1, 'B', 40), Group(2, 'A', 2), Group(3, 'B', 8), Group(4, 'A', 4), Group(5, 'B', 6) 
<br><br>
Where the first position represents the group id, the second the group label and the last one the group size (or amount of video slices in our case).
<br><br>
The total size of samples amout to 100. in a 80:10:10 train, eval, test split we would have 80 samples for train, 10 for eval and 10 for test. We use `priority` in the name of our algorithm because we prioritize the smaller split sets, solving them first, leaving the groups that are left to the bigger ones. So we might begin with the `eval` split.
<br><br>
For class `A` we have the following groups available:
<br><br>
Group(0, 'A', 40), Group(2, 'A', 2),Group(4, 'A', 4)
<br><br>
We need a subset of those groups that amout to 10, which is the size of our eval. Since we want it stratified, that is, proportional to the classes A and B, our target value will be 10% the size of class A, which is roud(0.1*46) = 5 . We use the subset sum algorithm to return the set which sum is closer to that value:
`Group(4, 'A', 4)`.
<br><br>
For class `B` we have the following groups available:
<br><br>
Group(1, 'B', 40),  Group(3, 'B', 8), Group(5, 'B', 6) 
<br><br>
Our target value will be round(0.1*54)=5. Wich yields `Group(5, 'B', 6)`
<br><br>
So for the eval set our algorithm returned Group(4, 'A', 4) and Group(5, 'B', 6), since 4 + 6 amounts to 10 and we've got a distribution of almost 50% percent of the slices for each class, this is an optimal solution.

## Usage
As desmostrated in the example a group in our implementation in defined as `Group(ID, CLASS, SIZE)`. A set of groups is represented by the class `GroupSet`, wich expects a list of `Group`s. The function `get_split` receives the`GroupSet` that represent your dataset and the split you want to create, which would be `[0.8, 0.1, 0.1]` in our exaple. `get_split` returns a list of `GroupSet`s that correspond to the specified split. 