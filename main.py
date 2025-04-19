from itertools import combinations

def compute_set_ratios(sets, original_ratios):
    n = len(sets)
    result = {}

    # Generate all possible combinations of sets
    for r in range(1, n + 1):
        for indices in combinations(range(n), r):
            # Step 1: Find common elements in the selected sets
            common = set.intersection(*[sets[i] for i in indices])
            other_indices = set(range(n)) - set(indices)
            
            # Step 2: Remove elements from other sets
            for other_i in other_indices:
                common -= sets[other_i]
            
            # Step 3: Generate the key (e.g., "common_in_set_1_set_3")
            key = "common_in_" + "_".join(f"set_{i+1}" for i in indices)
            
            # Step 4: Adjust the ratio list for the current combination
            included_ratios = [original_ratios[i] for i in indices]
            total = sum(included_ratios)
            keys = [str(i+1) for i in indices]
            adjusted_ratios = [ratio / total for ratio in included_ratios]
            my_dict = {k: v for k, v in zip(keys, adjusted_ratios)}  # Combine lists into a dict
            
            # Step 5: Store the common elements and adjusted ratios
            result[key] = {
                "elements": common,
                "ratios": my_dict
            }
    
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

def main():
    total = int(input("Enter the total electricity bill of this month: "))
    roomates = int(input("Enter the number of roomates: "))
    days_in_month = int(input("Enter the number days of this month: "))
    pay_per_day = float(total) / float(days_in_month)

    ratio_list = []
    bill_list = []
    duration_list = []
    # Get each person's ratio (depending on who use more electricity)
    for i in range(roomates):
        ratio_list.append(float(input(f"Enter ratio for person {i+1}: ")))


    # Get duration of stay each month
    print("Enter duration in format: dd-dd (for example: 01-31)")
    print("If a person has multiple durations, separate them using a comma: dd-dd,dd-dd,dd-dd (for example: 01-10,15-31)")
    for i in range(roomates):
        duration_list.append(input(f"Enter range of days for person {i+1}: "))


    
    my_set = list_to_set(duration_to_list(duration_list))
    result = compute_set_ratios(my_set, ratio_list)
    print(result)
    for i in range(roomates):
        topay = 0
        for k, v in result.items():
            days = len(v["elements"])
            ratios = v["ratios"]
            if str(i+1) in k:
                topay += pay_per_day * ratios[str(i+1)] * days
        bill_list.append(topay)

    print(bill_list)

main()