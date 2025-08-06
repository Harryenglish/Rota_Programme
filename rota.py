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

# Toy data has been imported

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
      employee.append(name)
      availability = []
      for col in shift_columns:
            confirmed = row[col]
            availability.append(confirmed.lower().strip() == "yes")
      
      emp = Employee(name, availability)
      employee.append(emp)

      
# for emp in employee:
#     print(emp)


# Employee class complete




# Do the schedular !!!


# Classify each morning, afternoon and evening shifts in the schedular



class Schedular:
      '''
      Classify which shifts are morning, afternoon and evening. 
      Check least available shifts to most.
      Show which shifts havent been taken.
      No shifts twice and maximum one a day.

      Ultimately a constraint satisfaction problem. Backtracking with Heuristics.
      '''
      def __init__(self, ):