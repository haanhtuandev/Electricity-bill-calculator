from itertools import combinations
from colorama import Fore, Style, init
import os
from art import *
import streamlit as st


st.text("Advanced Electricity Bill Splitter")

# Initialize colorama
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    clear_screen()
    tprint("Make it fair")
    print(Fore.YELLOW + "=" * 60)
    print(Fore.GREEN + "  Advanced Electricity Bill Splitting Calculator")
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
    print()

def compute_set_ratios(sets, original_ratios):
    n = len(sets)
    result = {}

    for r in range(1, n + 1):
        for indices in combinations(range(n), r):
            common = set.intersection(*[sets[i] for i in indices])
            other_indices = set(range(n)) - set(indices)
            
            for other_i in other_indices:
                common -= sets[other_i]
            
            key = "common_in_" + "_".join(f"set_{i+1}" for i in indices)
            included_ratios = [original_ratios[i] for i in indices]
            total = sum(included_ratios)
            keys = [str(i+1) for i in indices]
            adjusted_ratios = [ratio / total for ratio in included_ratios]
            my_dict = {k: v for k, v in zip(keys, adjusted_ratios)}
            
            result[key] = {
                "elements": common,
                "ratios": my_dict
            }
    
    return result

def list_to_set(lists):
    sets = []
    for lst in lists:
        flat_list = []
        for item in lst:
            if isinstance(item, list):
                flat_list.extend(item)
            else:
                flat_list.append(item)
        sets.append(set(flat_list))
    return sets

def duration_to_list(duration_list):
    range_list = []
    for duration in duration_list:
        if "," in duration:
            sub_ranges = duration.split(",")
            sub_range_list = []
            for sub in sub_ranges:
                try:
                    first, second = sub.split("-")
                    sub_range_list.append(list(range(int(first), int(second)+1)))
                except:
                    continue
            range_list.append(sub_range_list)
        else:
            try:
                first, second = duration.split("-")
                range_list.append(list(range(int(first), int(second)+1)))
            except:
                range_list.append([])
    return range_list

def get_valid_input(prompt, input_type=float, min_val=None, max_val=None):
    while True:
        try:
            value = input_type(input(prompt))
            if min_val is not None and value < min_val:
                raise ValueError(f"Value must be at least {min_val}")
            if max_val is not None and value > max_val:
                raise ValueError(f"Value must be at most {max_val}")
            return value
        except ValueError as e:
            print(Fore.RED + f"Invalid input: {e}. Please try again.")

def display_results(bill_list, total):
    print("\n" + Fore.YELLOW + "=" * 60)
    print(Fore.CYAN + "  BILL DISTRIBUTION RESULTS")
    print(Fore.YELLOW + "=" * 60)
    
    total_calculated = sum(bill_list)
    discrepancy = total - total_calculated
    
    # Display initial amounts
    for i, amount in enumerate(bill_list, 1):
        print(Fore.GREEN + f"  Person {i}: {Fore.WHITE}{amount:.2f} VND")
    
    print(Fore.YELLOW + "-" * 60)
    print(Fore.CYAN + f"  Total bill: {Fore.WHITE}{total:.2f} VND")
    print(Fore.CYAN + f"  Calculated total: {Fore.WHITE}{total_calculated:.2f} VND")
    
    if abs(discrepancy) > 0.01:
        print(Fore.RED + f"  Note: Rounding discrepancy of {discrepancy:.2f} VND")
        
        # Calculate proportional distribution weights
        weights = [bill/total_calculated for bill in bill_list] if total_calculated != 0 else [1/len(bill_list)]*len(bill_list)
        
        # Distribute discrepancy proportionally
        adjustments = [round(discrepancy * weight, 2) for weight in weights]
        
        # Ensure the sum of adjustments exactly matches the discrepancy
        adjustments[-1] += discrepancy - sum(adjustments)
        
        # Apply adjustments
        for i in range(len(bill_list)):
            bill_list[i] += adjustments[i]
        
        print(Fore.YELLOW + "  Proportional adjustments:")
        for i, adj in enumerate(adjustments, 1):
            print(Fore.CYAN + f"    Person {i}: {Fore.WHITE}{adj:+.2f} VND")
        
        print(Fore.YELLOW + "-" * 60)
        print(Fore.GREEN + "  Adjusted amounts:")
        for i, amount in enumerate(bill_list, 1):
            print(Fore.GREEN + f"    Person {i}: {Fore.WHITE}{amount:.2f} VND")
    
    print(Fore.YELLOW + "=" * 60 + "\n")

def main():
    display_header()
    
    # Get basic information
    print(Fore.CYAN + "STEP 1: Enter Basic Information")
    print(Fore.YELLOW + "-" * 60)
    total = get_valid_input("Enter total electricity bill (VND): ", float, 0)
    roommates = get_valid_input("Enter number of roommates: ", int, 1)
    days_in_month = get_valid_input("Enter number of days in this month: ", int, 1, 31)
    pay_per_day = float(total) / float(days_in_month)
    
    # Get ratios
    print("\n" + Fore.CYAN + "STEP 2: Enter Usage Ratios")
    print(Fore.YELLOW + "-" * 60)
    print(Fore.WHITE + "Enter each person's usage ratio (e.g., 0.3 is 30%, 1 is 100%)")
    ratio_list = []
    for i in range(roommates):
        ratio = get_valid_input(f"Enter ratio for Person {i+1}: ", float, 0.1)
        ratio_list.append(ratio)
    
    # Get duration of stay
    print("\n" + Fore.CYAN + "STEP 3: Enter Duration of Stay")
    print(Fore.YELLOW + "-" * 60)
    print(Fore.WHITE + "Format options:")
    print(" - Single range: dd-dd (e.g., 01-31)")
    print(" - Multiple ranges: dd-dd,dd-dd (e.g., 01-15,20-31)")
    print(" - Leave empty if not staying at all\n")
    
    duration_list = []
    for i in range(roommates):
        while True:
            duration = input(f"Enter day ranges for Person {i+1}: ").strip()
            if not duration:
                duration_list.append("")
                break
            try:
                # Validate format
                if any(not part.replace("-", "").isdigit() for part in duration.replace(",", "-").split("-")):
                    raise ValueError
                duration_list.append(duration)
                break
            except ValueError:
                print(Fore.RED + "Invalid format. Please try again.")
    
    # Calculate and display results
    print("\n" + Fore.CYAN + "Calculating...")
    my_set = list_to_set(duration_to_list(duration_list))
    result = compute_set_ratios(my_set, ratio_list)

    bill_list = []
    for i in range(roommates):
        topay = 0
        for v in result.values():
            days = len(v["elements"])
            ratios = v["ratios"]
            if str(i+1) in ratios:
                topay += pay_per_day * ratios[str(i+1)] * days
        # Only round the final amount
        bill_list.append(round(topay, 2))
    
    display_results(bill_list, total)
    
    # Wait before exiting
    input(Fore.YELLOW + "Press Enter to exit..." + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nProgram interrupted. Exiting...")
        exit()