# Grouped Stratified Split
Authors: [Felipe Marra](https://github.com/FelipeMarra) & [João Medrdo](https://github.com/jpmedras)
## About
This package solves the problem of performing a stratified split in a grouped dataset. This is a Multiple Subset Sum Problem (MSSP), which is considered to be strongly NP-hard. Although impossible to be solved optimally, this package presents an efficient and simple method based on Subset Sum iterations. We also implement a Greedy baseline.

A more comprehensive read about the problem and how the solution was designed can be found at [this blog post](https://medium.com/@felipeferreiramarra/stratified-split-for-grouped-datasets-with-dynamic-programming-76928a5f7eca).

## Usage
A group in our implementation in defined as `Group(ID, CLASS, SIZE)`. A set of groups is represented by the class `GroupSet`, wich expects a list of `Group`s. The function `get_split` receives the`GroupSet` that represent your dataset and the split you want to create, which may be `[0.8, 0.1, 0.1]` for exaple. `get_split` returns a list of `GroupSet`s that correspond to the specified split.
```Python
groups = [Group(0, 'A', 40), Group(1, 'B', 40), Group(2, 'A', 2), Group(3, 'B', 8), Group(4, 'A', 4), Group(5, 'B', 6)]
groups = GroupSet(groups)

priority_split = PrioritySplit()
sets = priority_split.get_split(groups, [0.8, 0.1, 0.1])

print(sets)
# Displays: [GroupSet({Group(0, A, 40), Group(1, B, 40)}), GroupSet({Group(4, A, 4), Group(5, B, 6)}), GroupSet({Group(2, A, 2), Group(3, B, 8)})]
```
To use the Greedy solution just instanciate the `GreedySplit` class instead of `PrioritySplit`.
