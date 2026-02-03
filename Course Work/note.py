"""Script to calculate Coursework marks needed
   to pass the module and to get a merit
   CSN08114/CSN08414, Nov 2022
"""
import sys


TEST_MAX_MARKS = 25  # max marks for test
TEST_WEIGHT = 0.4  # weight of test
CW_MAX_MARKS = 40  # max marks for CW
CW_WEIGHT = 0.6  # CW weight

print("To start, please enter your marks for the class test.\n",
      f"Make sure you enter the actual marks out of {TEST_MAX_MARKS}.")
test_marks = float(input(f"Enter the test marks: "))
if test_marks <= TEST_MAX_MARKS and test_marks >= 0:
    print("Thank you")
else:
    while test_marks > TEST_MAX_MARKS or test_marks < 0:
        print("Invalid number entered, try again")
        test_marks = float(input(f"Enter the test marks: "))

test_percent = test_marks/TEST_MAX_MARKS
needed_perc = (0.4 - test_percent*TEST_WEIGHT)/CW_WEIGHT
merit_perc = (0.65 - test_percent*TEST_WEIGHT)/CW_WEIGHT
needed = needed_perc * CW_MAX_MARKS + 0.1  # add 0.1 to avoid rounding issues

print(f"To pass the module (40%), you need {needed:2.1f} marks for the CW.")
if merit_perc <= 1:
    print(f"To get a merit (65%), you need {merit_perc*CW_MAX_MARKS:2.1f} marks for the CW.")
else:
    print(f"Unfortunately your test score is so poor that you cannot achieve a merit for the module")

