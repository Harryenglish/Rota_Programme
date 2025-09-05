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
        self.assigned = {day: {period: [] for period in PERIODS} for day in DAYS}

    def is_available(self, day, period):
        '''
        Check if this employee is available in a given day and period
        '''
        if period is None:
            return any(
                self.availability.get((day, p), False) 
                for p in ["Morning", "Afternoon", "Evening"])
        else:
            return self.availability.get((day, period), False)
        
    def available_employees(employees, day, period):
        '''
        Return names of employees available in a given day and period
        '''
        return [emp for emp in employees if employees[emp].is_available(day, period)]
    
    def assigned_count(self):
        return sum(len(shifts) for day_shifts in self.assigned.values() for shifts in day_shifts.values())
    
    def can_work(self, day, period):
        if self.is_available(day, period) == False:
            return False
        
        if any(self.assigned[day][p] for p in PERIODS):
            return False
        
        idx = DAYS.index(day)
        prev_day = DAYS[idx - 1]
        next_day = DAYS[min(6, (idx + 1))]

        if self.assigned[day]["Evening"] and self.assigned[next_day]["Morning"]:
            return False

        if self.assigned[day]["Morning"] and self.assigned[prev_day]["Evening"]:
            return False
        
        else:
            return True
        
    def assign(self, day, period, shift):
        self.assigned[day][period].append({
            "department": shift.department,
            "time_range": shift.time_range
        })

    def unassign(self, day, period, shift):
        self.assigned[day][period].remove({
            "department": shift.department,
            "time_range": shift.time_range
        })

    def __repr__(self):
        return f"Employee(Name = {self.name}, Availability = {self.availability})"
    


def employee_dictionary():

    employees = {}
    shift_columns = df.columns[1:]

    # Loop through 'Names' to get all the names. Then loop through all the shifts to get availability.

    for i, row in df.iterrows():
        name = row['Name']
        availability = []
        people = []
        for col in shift_columns:
            confirmed = row[col]
            availability.append(confirmed)     
        
        emp = Employee(name, availability)
        people.append(emp)

        employees[name] = Employee(name, availability)  

    return employees    

employees = employee_dictionary()

# print(employees)


# We can now find the availability of people on a given period

#for emp in employees:
#    test = employees[emp].assigned
#    print(test)






















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

    def assign(self, employee):
        self.assigned.append(employee)

    def unassign(self, employee):
        self.assigned.remove(employee)

    def __repr__(self):
        return f"Shift({self.period}, {self.time_range}, dept={self.department}, assigned={self.assigned})"
    



def shift_dictionary():    
    all_shifts = {}
    index_to_label = {}

    i = 0 
    for day in DAYS:
        all_shifts[day] = {period: [] for period in PERIODS}
        for period, times in zip(PERIODS, [morning_required, afternoon_required, evening_required]):
            for time in times:
                shift = Shift(period, time, department_mapping[time], day)
                all_shifts[day][period].append(shift)
                index_to_label[i] = (day, period, time, department_mapping[time])
                i += 1

    return all_shifts, index_to_label

all_shifts, index_to_label = shift_dictionary()

#print(all_shifts)
#print(index_to_label)





















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
          constrained_by_day = {}

          for day in DAYS:
            morning_count = 0
            afternoon_count = 0
            evening_count = 0
            for emp in employees:
                if employees[emp].availability[(day, "Morning")] == True:
                    morning_count += 1
                if employees[emp].availability[(day, "Afternoon")] == True:
                    afternoon_count += 1
                if employees[emp].availability[(day, "Afternoon")] == True:
                    evening_count += 1

            counts = [morning_count, afternoon_count, evening_count]
            period_count = list(zip(counts, PERIODS))
            sorted_count = sorted(period_count)

            constrained_by_day[day] = sorted_count    

          return constrained_by_day
      
      def available_candidates(self):
          '''
          With all available people together
          Find out of all of them who has the least many assignments
          Give them the next shift
          '''
          available_candidates = {}
          all_days_constraints = self.most_constrained()

          for day in DAYS:
              daily_dictionary = {}
              period_counts = all_days_constraints[day]
              for count, period in period_counts:  
                  daily_dictionary[period] = Employee.available_employees(employees, day, period)

              available_candidates[day] = daily_dictionary

          return available_candidates


    
      def least_assigned(self):
          '''
          Take available candidates dictionary
          Extract the lists of available candidates for any given period on any given day
          Sort and put into new dictionary in same format
          '''

          available_candidates = self.available_candidates()
          least_assigned = {}
          weekly_available = []

          for day, periods in available_candidates.items():
              daily_available = []
              for period, emp_list in periods.items():
                  daily_available.append(emp_list)
              weekly_available.append(daily_available)        


          all_names_sorted = []

          for i in range(len(DAYS)):
              daily_sorted = []
              for j in range(len(PERIODS)):
                  name_assign_count = [(emp, employees[emp].assigned_count()) for emp in weekly_available[i][j]]
                  sorted_count = sorted(name_assign_count, key=lambda x: x[1])
                  sorted_names = [emp for emp, count in sorted_count]
                  daily_sorted.append(sorted_names)
              all_names_sorted.append(daily_sorted)      
                  

          day_names = list(available_candidates.keys())  

          for day_idx, day in enumerate(day_names):
              period_order = list(available_candidates[day].keys())  
              least_assigned[day] = {}
              for period_idx, period in enumerate(period_order):
                  least_assigned[day][period] = all_names_sorted[day_idx][period_idx]
              
          return least_assigned
      
      def backtracking(self, day):
          '''
          This method is in charge of if any of the tests fail, this rebuilds the rota and makes it work !!!!!!!!
          '''
          least_assigned_day = self.least_assigned()[day]

          for period in least_assigned_day:
              for shift in all_shifts[day][period]:
                  for emp in least_assigned_day[period]:
                      self.employees[emp].unassign(day, period, shift)
                      self.shift.unassign(emp)
                      rota[day][period].remove({"employee": emp, "shift": shift})    
                      continue
                  
      def forward_checker(self, day, period):
          '''
          This method is in charge of looking into the future to prevent expensive unnecessary search spaces
          '''                
          remaining_shifts = [shift for shift in all_shifts[day][period] if not shift.assigned]
          available_emps = [emp for emp in self.employees
                            if self.employees[emp].can_work(day, period)]
          
          if len(available_emps) < len(remaining_shifts):
              if len(available_emps) == 0:
                  return False
              return True
          return True
          
      def rota_assigner(self):
          '''
          This method is in charge of assigning shifts
          If there is a conflict, the method will backtrack and schedule appropriately
          Checks if someone is assigned on that period, if not assign and mark rest of day off
          '''

          rota = {day: {period: [] for period in PERIODS} for day in DAYS}
                                     
          for day in DAYS:
              for period in self.least_assigned()[day]:
                  for shift in all_shifts[day][period]:
                      assign_confirmed = False
                      for emp in self.least_assigned()[day][period]:  
                          if not self.employees[emp].can_work(day, period):
                              continue                         
                          checkpoint = self.forward_checker(day, period) 
                          if checkpoint:
                              self.employees[emp].assign(day, period, shift)
                              shift.assign(emp)
                              rota[day][period].append({"employee": emp, "shift": shift})
                              assign_confirmed = True
                              break
                          if not assign_confirmed and not checkpoint:
                              self.employees[emp].unassign(day, period, shift)
                              shift.unassign(emp)
                              rota[day][period] = [entry for entry in rota[day][period] 
                                                   if entry["employee"] != emp or entry["shift"] != shift]
                              continue
                          
          return rota
      
      def get_unassigned_shifts(self):
            
            rota = self.rota_assigner()
            unassigned_dict = {day: {period: [] for period in PERIODS} for day in DAYS}

            for day in DAYS:
                for period in PERIODS:
                    unassigned = [
                        shift for shift in all_shifts[day][period]
                        if not any(assignment['shift'] == shift for assignment in rota[day][period])]
                    if unassigned:
                        unassigned_dict[day][period] = unassigned

            return unassigned_dict
      
      def export_rota_to_excel(self, filename="rota.xlsx"):
            # First, figure out all departments
            rota = self.rota_assigner()

            departments = set()
            for day in rota:
                for period in rota[day]:
                    for item in rota[day][period]:
                        departments.add(item["shift"].department)

            # Create a dictionary of DataFrames per department
            dept_sheets = {dept: [] for dept in departments}

            for dept in departments:
                for day in rota:
                    for period in rota[day]:
                        shifts = [item for item in rota[day][period] if item["shift"].department == departments]
                        if shifts:
                            for item in shifts:
                                dept_sheets[dept].append({
                                    "Day": day,
                                    "Period": period,
                                    "Employee": item["employee"],
                                    "Shift Time": str(item["shift"])
                                })
                        else:
                            # Optional: show unassigned shifts
                            dept_sheets[dept].append({
                                "Day": day,
                                "Period": period,
                                "Employee": "UNASSIGNED",
                                "Shift Time": ""
                            })

            # Write to Excel
            #with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            #    for dept, data in dept_sheets.items():
            #        df = pd.DataFrame(data)
            #        df.to_excel(writer, sheet_name=dept[:31], index=False)
          

                    

# make sure backtesting behaviour is sound, no infinite loops, breaking where appropriate
# check rota assigner to make sure logic is sound, make sure each method talks to eachother correctly 
# build back tracker with correct logic
# export

# build forward checker
# build back tracker
# check assigner logic






rota = Scheduler(employees, all_shifts)
print(rota.rota_assigner())






# check forward checking, backtracking and assigner logic
# add comments
# export to excel 
# do another test with new data