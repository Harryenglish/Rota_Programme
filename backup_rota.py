import pandas as pd

# Work week starts on Friday and staff can only give availability as morning, afternoon and evening for each day

DAYS = ["Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
PERIODS = ["Morning", "Afternoon", "Evening"]

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
    "17:00 - 00:00": "Sushisamba"}

# Creating an index for a shift dictionary

index_to_label = {
    i: (day, period)
    for day_index, day in enumerate(DAYS)
    for period_index, period in enumerate(PERIODS)
    for i in [day_index * len(PERIODS) + period_index]}




# Importing the google form as excel sheet

df = pd.read_excel("test.xlsx")

# Removing timestamp column, changing Name column name, changing yes and no string to boolean

df.columns.values[1] = 'Name'
del df[df.columns[0]]
initial_columns = df.columns[1:]

for col in initial_columns:
    for index, row in df.iterrows():
        if str(row[col]).lower().strip() == "yes":
            df.at[index, col] = True
        else:
             df.at[index, col] = False
    
# Employee class

class Employee:
    '''
    This class concerns the state of all employees

    Employee class has properties - name, availability and assigned shifts
    It will be able to see what shifts someone is available for
    Assign and unassign shifts (one shift a day)
    Check how many shifts a person has throughout the scheduling process
    Check if someone has a shift on a given day
    Show what availability a person has after the scheduling process 
    Mark unavailable for clopens
    '''
    def __init__(self, name, availability_flat):
        self.name = name
        self.availability = {
            index_to_label[i]: available
            for i, available in enumerate(availability_flat)}
        self.assigned = []

    def is_available(self, day, period):
        '''
        Check if this employee is available in a given day and period
        '''
        return self.availability.get((day, period), False)
    
    def available_employees(employees, day, period):
        '''
        Return names of employees available in a given day and period
        '''
        return [emp.name for emp in employees if emp.is_available(day, period)]
        


    def __repr__(self):
        return f"Employee(Name = {self.name}, Availability = {self.availability})"
    


def employee_dictionary():

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

    return employees    

employees = employee_dictionary()

# print(employees)


# We can now find the availability of people on a given period

# yes = Employee.available_employees(employees, "Saturday", "Evening")
# print(yes)



# Shifts class

class Shift:
    '''
    This class concerns everything to do with the shifts themselves

    Contains info on the shift period, time, department and day
    Mark a shift assigned 
    Mark a shift not assigned
    Check if a shift has someone assigned
    If a shift has nobody to fill it, show
    '''
    def __init__(self, period, time_range, department, day):
        self.period = period 
        self.time_range = time_range
        self.department = department
        self.day = day
        self.assigned = []
        self.unassignable = False

    def __repr__(self):
        return f"Shift({self.period}, {self.time_range}, dept={self.department}, assigned={self.assigned})"
    



def shift_dictionary():    
    all_shifts = []
    index_to_label = {}

    i = 0 
    for day in DAYS:
        for period, times in zip(PERIODS, [morning_required, afternoon_required, evening_required]):
            for time in times:
                shift = Shift(period, time, department_mapping[time], day)
                all_shifts.append(shift)
                index_to_label[i] = (day, period, time, department_mapping[time])
                i += 1

    return all_shifts, index_to_label

all_shifts, index_to_label = shift_dictionary()

# print(all_shifts)
# print(index_to_label)






# Schedular class


class Scheduler:
      '''
      The Scheduler class will be in charge of finding people for a shift

      It will use backtracking with heuristics to schedule shifts
      Finds most constrained shift 
      Access employee and shifts data
      Finds least assigned person
      Access methods in employee and shift classes to mark shifts assigned
      And to mark a shift not assigned
      Check if a shift has anyone assigned to it
      If a shift has nobody to fill it do backtracking once, if fail then mark unassigned
      '''
      def __init__(self, employees, all_shifts):
        self.employees = employees
        self.all_shifts = all_shifts

      def most_constrained(self):
          constrained_by_day = []

          for day in DAYS:
              morning_count = 0
              afternoon_count = 0
              evening_count = 0
              for emp in employees:                
                  if emp.availability[(day, "Morning")] == True:
                      morning_count += 1
                  if emp.availability[(day, "Afternoon")] == True:
                      afternoon_count += 1
                  if emp.availability[(day, "Evening")] == True:
                      evening_count += 1

              counts = [morning_count, afternoon_count, evening_count]
              period_count = list(zip(counts, PERIODS))
              sorted_count = sorted(period_count)

              constrained_by_day.append(sorted_count)    

          return constrained_by_day
      
      def get_least_assigned():
          



          return least_assigned_employee




#rota = Scheduler(employees, all_shifts)
#print(rota.most_constrained())




# find the least assigned person as a method in scheduler and start scheduling that period from there !