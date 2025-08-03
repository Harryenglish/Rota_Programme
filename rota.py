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

# Toy data has been imported

# Now we need a way of classifying every employee and their availability (by mapping 'yes' to True and 'no' to False)

class Employee:
        '''
        All that is gathered from the form is name and availability. So we will make this our object.
        '''
        def __init__(self, employee, availability):
            self.employee = employee
            self.availability = availability 
            self.assigned = []

employee = []


# Loop through 'Names' to get all the names. Then loop through all the shifts to get availability.

for i, row in df.iterrows():
      name = row['Name']
      employee.append(name)
      for j, column in 

            






# we have imported the data now we need to use a boolean system to know when shifts can be done and who it is that is available

# then we make the schedular !!!