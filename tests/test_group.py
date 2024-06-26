from src.priority_group_stratified_split.group_set import Group, GroupSet

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

groups1 = GroupSet(groups1)
groups2 = GroupSet(groups2)


#print(groups1, groups1.total_size)
#print()

#print(groups2, groups2.total_size)
#print()

################# 
# Test GroupSet Creation
#################
def test_group_set_creation():
    assert groups1.total_size == sum(range(0, 5))
    assert groups2.total_size == sum(range(5, 10))

    assert groups1.get_uids() == [0, 1, 2, 3, 4]
    assert groups2.get_uids() == [5, 6, 7, 8, 9]

    assert len(groups1.get_label_indexer()['B']) == 3
    assert len(groups1.get_label_indexer()['C']) == 2

    assert len(groups2.get_label_indexer()['B']) == 3
    assert len(groups2.get_label_indexer()['A']) == 1
    assert len(groups2.get_label_indexer()['C']) == 1

################# 
# Test Set Subtraction
#################
def test_group_set_subtraction(): 
    groups3 = (groups1 | groups2) - groups2
    assert groups3 == groups1

################# 
# Test Add
#################
def test_group_set_add():
    groups1.add(Group(10, 'C', 2))

    assert groups1.total_size == sum(range(0, 5)) + 2
    assert groups1.get_uids() == [0, 1, 2, 3, 4, 10]
    assert len(groups1.get_label_indexer()['B']) == 3
    #print("###################################")
    #print(groups1)
    #print(groups1.get_label_indexer()['C'])
    assert len(groups1.get_label_indexer()['C']) == 3

################# 
# Test Indexers
#################
uid_indexer1 = groups1.get_uid_indexer()
#print(uid_indexer1[0])
#print(uid_indexer1[3])
#print(uid_indexer1[10])
#print()

label_indexer1 = groups1.get_label_indexer()
#print(label_indexer1['B'])
#print(label_indexer1['C'])
#print(label_indexer1['A'])
#print()