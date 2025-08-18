import pandas as pd


# any magic numbers must be declared 

# We need to get some initial data

# Create new data frame with 23 entries


# Import the data from a google form and bring it into a data frame
# First take the data, find each employee and their availability
# Then assign shifts based off availability using the schedular
# Check that all contraints are satisfied 
# ^ (people get as many shifts as possible, maximum shifts are occupied, no shifts given twice, only one shift a day)
# Eventually export the rota to a spreadsheet


DAYS = ["Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
PERIODS = ["Morning", "Afternoon", "Evening"]

index_to_label = {
    i: (day, period)
    for day_index, day in enumerate(DAYS)
    for period_index, period in enumerate(PERIODS)
    for i in [day_index * len(PERIODS) + period_index]
}


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

# Now we need a way of classifying every employee and their availability 

class Employee:
        '''
        All that is gathered from the form is name and availability. So we will make this our object.

        The purpose of this class is so we can access availability information as efficiently as possible.
        '''
        def __init__(self, employee, availability_flat):
            self.employee = employee
            self.availability = {
            index_to_label[i]: available
            for i, available in enumerate(availability_flat)
        } 
            self.assigned = []

        def __repr__(self):
            return f"Employee(name={self.employee}, availability={self.availability})"    

employees = []
shift_columns = df.columns[1:]

# Loop through 'Names' to get all the names. Then loop through all the shifts to get availability.

for i, row in df.iterrows():
      name = row['Name']
      availability = []
      for col in shift_columns:
            confirmed = row[col]
            availability.append(confirmed)     
      
      emp = Employee(name, availability)
      employees.append(emp)

      

# print(employees)


# Employee class complete

class Shift:
    def __init__(self, period, time_range, department, day):
        self.period = period 
        self.time_range = time_range
        self.department = department
        self.day = day
        self.assigned = []

    def __repr__(self):
        return f"Shift({self.period}, {self.time_range}, dept={self.department}, assigned={self.assigned})"
    
morning_required = ["7:00 - 13:00", "10:00 - 18:00", "8:00 - 13:00", "9:00 - 17:00"]
afternoon_required = ["16:00 - 00:00", "12:00 - 22:00", "14:00 - 23:00"]
evening_required = ["17:00 - 01:00", "17:00 - 00:00"]

department_mapping = {
    "7:00 - 13:00": "Sushisamba",
    "10:00 - 18:00": "W Lounge",
    "8:00 - 13:00": "Sushisamba",
    "12:00 - 22:00": "W Lounge",
    "9:00 - 17:00": "Sushisamba",
    "14:00 - 23:00": "W Lounge",
    "16:00 - 00:00": "Sushisamba",
    "17:00 - 01:00": "W Lounge",
    "17:00 - 00:00": "Sushisamba"
}

all_shifts = []

for time in morning_required:
    all_shifts.append(Shift("morning", time, department_mapping[time]))
for time in afternoon_required:
    all_shifts.append(Shift("afternoon", time, department_mapping[time]))
for time in evening_required:
    all_shifts.append(Shift("evening", time, department_mapping[time]))

# print(all_shifts)

# Shift class complete




# Schedular class


class Scheduler:
      '''
      Check least available shifts to most, and assign accordingly.
      No shifts twice and maximum one a day.
      Show which shifts havent been taken.
      Show whos available but havent been assigned.
      
      
      Ultimately a constraint satisfaction problem. Backtracking with Heuristics.
      '''
      def __init__(self, employees, all_shifts):
        self.employees = employees
        self.all_shifts = all_shifts

      def Scheduling(self):
        
      
      
      def Exporter(self, all_assigned):
          '''
          This method will be in charge of exporting the rota into a viewable format

          Assign shift times to department
          '''
          
              
        



