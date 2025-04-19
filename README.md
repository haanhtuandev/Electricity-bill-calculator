# Make It Fair - Advanced Electricity Bill Splitting Calculator

## Overview
"Make It Fair" is a sophisticated command-line utility designed to help students in VGU dormitories split electricity bills with maximum fairness. The calculator accounts for:

- Variable usage ratios between roommates
- Different durations of stay during the billing period
- Multiple occupancy periods (people coming and going)

This tool ensures that everyone pays their fair share based on both their actual usage patterns and the time they were present in the shared space.

## Features

- **Usage-Based Calculation**: Assign different ratios to roommates who use more or less electricity
- **Partial Stay Support**: Calculate fair amounts for roommates who weren't present for the full billing period
- **Complex Stay Patterns**: Handle scenarios where roommates stay for non-consecutive periods
- **Automatic Discrepancy Adjustment**: Proportionally distributes any rounding differences
- **User-Friendly Interface**: Colorful, guided interface with clear input instructions
- **Elegant Visual Presentation**: Uses ASCII art and color-coded results for better readability

## Requirements

- Python 3.6+
- Required packages:
  - `colorama`: For colored terminal output
  - `art`: For ASCII text art
  - `itertools`: Standard Python library for iterator building blocks

## Installation

1. Clone this repository or download the source code
2. Install the required packages:

```bash
pip install colorama art
```

## Usage

Run the program using Python:

```bash
python main.py
```

Follow the on-screen prompts to:

1. Enter the total electricity bill amount
2. Input the number of roommates
3. Specify the number of days in the month
4. Assign usage ratios for each roommate
5. Enter the duration of stay for each person

### Duration Format Options

The calculator supports various stay patterns:
- Single range: `01-31` (stayed from 1st to 31st)
- Multiple ranges: `01-15,20-31` (stayed from 1st to 15th and from 20th to 31st)
- Leave empty if not present at all during the billing period

## How It Works

The application uses set theory and combinatorial mathematics to:

1. Convert each roommate's stay duration into sets of days
2. Calculate intersections between these sets to determine periods of shared occupancy
3. Adjust the payment ratios within each shared period
4. Calculate the per-day cost and apply appropriate ratios and durations
5. Sum up the total owed by each roommate
6. Distribute any rounding discrepancies proportionally

## Example

```
======================================================
  Advanced Electricity Bill Splitting Calculator
======================================================

STEP 1: Enter Basic Information
------------------------------------------------------
Enter total electricity bill (VND): 500000
Enter number of roommates: 3
Enter number of days in this month: 30

STEP 2: Enter Usage Ratios
------------------------------------------------------
Enter each person's usage ratio (e.g., 0.3 is 30%, 1 is 100%)
Enter ratio for Person 1: 1
Enter ratio for Person 2: 1.5
Enter ratio for Person 3: 0.8

STEP 3: Enter Duration of Stay
------------------------------------------------------
Format options:
 - Single range: dd-dd (e.g., 01-31)
 - Multiple ranges: dd-dd,dd-dd (e.g., 01-15,20-31)
 - Leave empty if not staying at all

Enter day ranges for Person 1: 01-30
Enter day ranges for Person 2: 10-30
Enter day ranges for Person 3: 01-15

Calculating...

======================================================
  BILL DISTRIBUTION RESULTS
======================================================
  Person 1: 250000.00 VND
  Person 2: 175000.00 VND
  Person 3: 75000.00 VND
------------------------------------------------------
  Total bill: 500000.00 VND
  Calculated total: 500000.00 VND
======================================================
```

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements or bug fixes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created by Tuan Ha to help VGU dormitory residents split bills fairly.