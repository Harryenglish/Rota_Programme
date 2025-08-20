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
    Show what availability a person has after the scheduling process 
    No clopens!!!
    '''
    def __init__(self, name, availability_flat):
        self.name = name
        self.availability = {
            index_to_label[i]: available
            for i, available in enumerate(availability_flat)}
        self.assigned = []

# happy with above in class




    def is_available_for(self, day, period):              # Revise
        # Check if employee is available for this shift AND hasn't already been assigned today
        available_today = self.count_assigned_on(day) < 1
        return (day, period) in self.availability and available_today

    def count_assigned_on(self, day):                  # Revise         
        # Count how many shifts already assigned on this day
        return sum(1 for shift in self.assigned if shift.day == day)

    def mark_unassigned(self, shift):              # Revise
        # Optional: remove shift from assigned if needed
        if shift in self.assigned:
            self.assigned.remove(shift)

    def __repr__(self):
        return f"Employee(Name = {self.name}, Availability = {self.availability})"
    




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

      

# print(employees)







# Shifts class

class Shift:
    '''
    This class concerns everything to do with the shifts themselves

    Contains info on the shift period, time, department and day
    Mark a shift assigned/not assigned
    If a shift has nobody to fill it, show
    '''
    def __init__(self, period, time_range, department, day):
        self.period = period 
        self.time_range = time_range
        self.department = department
        self.day = day
        self.assigned = []

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

      It will use backtracking with heuristics
      Searching for most constrained shift and assigning least assigned available employee
      '''
      def __init__(self, employees, all_shifts):
        self.employees = employees
        self.all_shifts = all_shifts

      def Scheduling(self):
          assign = []
          return assign
        
        

      def get_candidates(self, shift):
        return [e for e in self.employees if e.is_available_for(shift.day, shift.period)]

      def count_available(self, shift, shift_index):
        return len(self.get_candidates(shift))








schedule_dict = {}

for shift in all_shifts:
    day = shift.day
    dept = shift.department
    if day not in schedule_dict:
        schedule_dict[day] = {}
    if dept not in schedule_dict[day]:
        schedule_dict[day][dept] = []
    schedule_dict[day][dept].append(shift)

# Flatten into rows for a DataFrame
rows = []
for day, depts in schedule_dict.items():
    for dept, shifts in depts.items():
        for shift in shifts:
            rows.append({
                "Day": day,
                "Department": dept,
                "Period": shift.period,
                "Time": shift.time_range,
                "Assigned": ", ".join([e.employee for e in shift.assigned]) or "Unassigned"
            })

df_schedule = pd.DataFrame(rows)

# print(df_schedule)

# Save to Excel
# df_schedule.to_excel("rota_schedule.xlsx", index=False)
