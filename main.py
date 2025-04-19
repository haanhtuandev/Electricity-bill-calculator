from itertools import combinations

def find_common_and_unique_elements(sets):
    n = len(sets)
    result = {}

    # Find elements unique to each set
    for i in range(n):
        other_sets = sets[:i] + sets[i+1:]
        unique = sets[i].copy()
        for s in other_sets:
            unique -= s
        result[f"only_in_set_{i+1}"] = [unique, 1]

    # Find elements common to combinations of sets
    for r in range(2, n+1):
        for indices in combinations(range(n), r):
            common = set.intersection(*[sets[i] for i in indices])
            other_indices = set(range(n)) - set(indices)
            for other_i in other_indices:
                common -= sets[other_i]
            key = "common_in_" + "_".join(f"set_{i+1}" for i in indices)
            result[key] = common

    return result

def list_to_set(lists):
    sets = []
    for lst in lists:
        # Flatten nested lists (if any)
        flat_list = []
        for item in lst:
            if isinstance(item, list):
                flat_list.extend(item)
            else:
                flat_list.append(item)
        sets.append(set(flat_list))
    return sets

def duration_to_list(duration_list):                        #l1                     #l2                         #l3 (with sublists)
    range_list = [] # range list will look like this [ [1,2,3,4,...,20] , [5,6,7,8,9,10,...,20] [[1,2,3,4,...15], [20,21,22,...,30]] ]
    # duration_list = ["01-10,15-31", "08-30", "14-28"]
    for i in range(len(duration_list)):
        if len(duration_list[i]) == 5:
            first_range = int((duration_list[i])[:2])
            second_range = int((duration_list[i])[3:])
            range_list.append(list(range(first_range, second_range+1)))
        elif len(duration_list[i]) > 5:
            duration_list[i] = duration_list[i].strip()
            sub_list = duration_list[i].split(",") # from "01-10,15-31" to ["01-10", "15-31"]
            print(f"This is sublist = {sub_list}")
            sub_range_list = []
            for sub in sub_list:
                print(f"This is first range: {sub[:2]}")
                print(f"This is second range: {sub[3:5]}")
                first_range = int(sub[:2])
                second_range = int(sub[3:5])
                sub_range_list.append(list(range(first_range, second_range+1)))
            range_list.append(sub_range_list)
        else:
            range_list.append(list(0))
    return range_list

# [[[1, 2, 3, 4, 5, 6, 7, 8, 9], [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]],
#  [[8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]],
#  [[14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]]]
        

# remember to handle cases where one person doesnt use electricity for the whole month

def split(total, roomates):
    ratio_list = []
    bill_list = []
    duration_list = []
    main_dict = {}
    # Get each person's ratio (depending on who use more electricity)
    for i in range(roomates):
        ratio_list.append(float(input(f"Enter ratio for person {i+1}: ")))


    # Get duration of stay each month
    print("Enter duration in format: dd-dd (for example: 01-31)")
    print("If a person has multiple durations, separate them using a comma: dd-dd,dd-dd,dd-dd (for example: 01-10,15-31)")
    for i in range(roomates):
        duration_list.append(input(f"Enter range of days for person {i+1}: "))
        # Get all possible 1,2,3,...n-element combinations of a list

    
    my_set = list_to_set(duration_to_list(duration_list))
    result = find_common_and_unique_elements(my_set)
    for k, v in result.items():
        print(f"{k}: {v}")


    return bill_list

split(100,3)