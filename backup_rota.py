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


df = pd.read_excel("test.xlsx")

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
    def __init__(self, name, availability):
        self.name = name
        # availability is a list of tuples: (day, period)
        # e.g., [('Monday', 'morning'), ('Tuesday', 'evening')]
        self.availability = availability  
        self.assigned = []

    def is_available_for(self, day, period):
        # Check if employee is available for this shift AND hasn't already been assigned today
        available_today = self.count_assigned_on(day) < 1
        return (day, period) in self.availability and available_today

    def count_assigned_on(self, day):
        # Count how many shifts already assigned on this day
        return sum(1 for shift in self.assigned if shift.day == day)

    def mark_unassigned(self, shift):
        # Optional: remove shift from assigned if needed
        if shift in self.assigned:
            self.assigned.remove(shift)

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
        self.unassignable = False

    def __repr__(self):
        return f"Shift({self.period}, {self.time_range}, dept={self.department}, assigned={self.assigned})"
    
    def status(self):
        print(self.assigned)
    
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

for day in DAYS:
    for time in morning_required:
        all_shifts.append(Shift("morning", time, department_mapping[time], day))
    for time in afternoon_required:
        all_shifts.append(Shift("afternoon", time, department_mapping[time], day))
    for time in evening_required:
        all_shifts.append(Shift("evening", time, department_mapping[time], day))

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
        sorted_shifts = sorted(enumerate(self.all_shifts),key=lambda x: self.count_available(x[1], x[0]))

        for shift_index, shift in enumerate([s for i, s in sorted_shifts]):
            candidates = self.get_candidates(shift)
            if not candidates:
                shift.unassignable = True
                continue

            employee = min(candidates, key=lambda e: len(e.assigned))
            shift.assigned.append(employee)
            employee.assigned.append(shift)

            for e in candidates:
                if e != employee:
                    e.mark_unassigned(shift)

      def get_candidates(self, shift):
        return [e for e in self.employees if e.is_available_for(shift.day, shift.period)]

      def count_available(self, shift, shift_index):
        return len(self.get_candidates(shift))
      
      
      
      
              
        
# scheduling class need method for heuristics, scheduling from most constrained
# least assigned employee, no shifts for one person twice in one day

# shifts need attribute that show if nobody can take it

# employee needs attribute that shows if they are available but not been assigned








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

print(df_schedule)

# Save to Excel
# df_schedule.to_excel("rota_schedule.xlsx", index=False)




# go through all classes and fix everything



# employee class holds all employee info, name, availability, what shifts theyve been assigned
# shifts class holds all shift info, department, what period maps to what shift time, time, whos doing it, day
# scheduler class is main csp solver, maximising shifts assigned and giving out shifts as evenly as possible