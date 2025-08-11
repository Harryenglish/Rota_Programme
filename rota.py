import numpy as np
import pandas as pd

# We need to get some initial data


# Import the data from a google form and bring it into a data frame
# First take the data, find each employee and their availability
# Then assign shifts based off availability using the schedular
# Check that all contraints are satisfied 
# ^ (people get as many shifts as possible, maximum shifts are occupied, no shifts given twice, only one shift a day)
# Eventually export the rota to a spreadsheet



df = pd.read_excel("rota data export (Responses).xlsx")

df.columns.values[1] = 'Name'
del df[df.columns[0]]
initial_columns = df.columns[1:]

for col in initial_columns:
    for index, row in df.iterrows():
        if str(row[col]).lower().strip() == "yes":
            df.at[index, col] = True
        else:
             df.at[index, col] = False
        


# Toy data has been imported and normalised

# Now we need a way of classifying every employee and their availability (by mapping 'yes' to True and 'no' to False)

class Employee:
        '''
        All that is gathered from the form is name and availability. So we will make this our object.

        The purpose of this class is so we can access availability information as efficiently as possible.
        '''
        def __init__(self, employee, availability):
            self.employee = employee
            self.availability = availability 
            self.assigned = []

        def __repr__(self):
            return f"Employee(name={self.employee}, availability={self.availability})"    

employee = []
shift_columns = df.columns[1:]

# Loop through 'Names' to get all the names. Then loop through all the shifts to get availability.

for i, row in df.iterrows():
      name = row['Name']
      availability = []
      for col in shift_columns:
            confirmed = row[col]
            availability.append(confirmed)     # Double check if this includes name column
      
      emp = Employee(name, availability)
      employee.append(emp)

      

# print(employee)


# Employee class complete







# Classify each morning, afternoon and evening shifts in the schedular


# classify validity of truth statements for morning afternoon and evening by sorting through in threes, then every 3 can be eligible for given shifts

# go through employee class, find name of each and store morning afternoon and evening data separately, like a subset of the class

def shift_classifier():

    morning_shifts = []
    afternoon_shifts = []
    evening_shifts = []

    for i, row in df.iterrows():
        names = row['Name']
        morning_availability = []
        for col in df.columns[1::3]:
             morning_confirmed = row[col]
             morning_availability.append(morning_confirmed)

        morning_shifts.append((names, morning_availability))
    
    for j, row in df.iterrows():
        names = row['Name']
        afternoon_availability = []
        for col in df.columns[2::3]:
             afternoon_confirmed = row[col]
             afternoon_availability.append(afternoon_confirmed)

        afternoon_shifts.append((names, afternoon_availability))

    for k, row in df.iterrows():
        names = row['Name']
        evening_availability = []
        for col in df.columns[3::3]:
             evening_confirmed = row[col]
             evening_availability.append(evening_confirmed)

        evening_shifts.append((names, evening_availability))    

    return morning_shifts, afternoon_shifts, evening_shifts


# test = print(shift_classifier())


# Schedular class


class Schedular:
      '''
      Classify which shifts are morning, afternoon and evening. 
      Check least available shifts to most, and assign accordingly.
      No shifts twice and maximum one a day.
      Show which shifts havent been taken.
      Show whos available but havent been assigned.
      
      
      Ultimately a constraint satisfaction problem. Backtracking with Heuristics.
      '''
      def __init__(self, employee, morning_shifts, afternoon_shifts, evening_shifts):
           self.employee = employee
           self.morning_shifts = morning_shifts
           self.afternoon_shifts = afternoon_shifts
           self.evening_shifts = evening_shifts
           self.assigned = []