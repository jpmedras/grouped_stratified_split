import sys
sys.path.append('./src/priority_group_stratified_split')

from groups import Group, Groups

groups_count = 0

def create_groups(n:int, seq_labels:int):
    global groups_count
    n += groups_count

    groups = []
    
    char_add = 0
    for i in range(groups_count, n):
        char_add = char_add +1 if i % seq_labels == 0 else char_add
        label = chr(65+char_add)
        groups.append(Group(i, label, i))

    groups_count += n

    return groups

groups1 = create_groups(5, 3)
groups2 = create_groups(5, 3)

groups1 = Groups(groups1)
groups2 = Groups(groups2)

print(groups1, groups1.total_size)
print()

print(groups2, groups2.total_size)
print()

groups3 = (groups1 | groups2) - groups2
print(groups3, groups3.total_size)
assert ((groups1 | groups2) - groups2) == groups1
print()

print(groups2.labels)
print()

################# 
# Test Add
#################
groups1.add(Group(10, 'C', 2))
print(groups1)
print()

################# 
# Test Indexers
#################
uid_indexer1 = groups1.get_uid_indexer()
print(uid_indexer1[0])
print(uid_indexer1[3])
print(uid_indexer1[10])
print()

label_indexer1 = groups1.get_label_indexer()
print(label_indexer1['B'])
print(label_indexer1['C'])
print(label_indexer1['A'])
print()