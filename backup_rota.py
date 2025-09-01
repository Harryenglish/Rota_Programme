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
        self.assigned = {}

    def is_available(self, day, period):
        '''
        Check if this employee is available in a given day and period
        '''
        return self.availability.get((day, period), False)
    
    def available_employees(employees, day, period):
        '''
        Return names of employees available in a given day and period
        '''
        return [emp for emp in employees if employees[emp].is_available(day, period)]
    
    def assigned_count(self):
        return len(self.assigned)
    
    def can_work(self, day, period, prev_day=None, prev_period=None):
        if not self.is_available(day, period):
            return False
        
        if day in self.assigned and self.assigned[day]:
            return False
        
        if prev_day and prev_period:
            if self.assigned.get(prev_day, []) and prev_period == "Evening" and period == "Morning":
                return False

        return True
        
    def assign(self, day, shift):
        if day not in self.assigned:
            self.assigned[day] = []
        self.assigned[day].append({
            "period": shift.period,
            "department": shift.department,
            "time_range": shift.time_range,
            })

    def unassign(self, day, shift):
        if day in self.assigned:
            self.assigned[day] = [
                s for s in self.assigned[day]
                if not (
                    s["period"] == shift.period and
                    s["department"] == shift.department and
                    s["time_range"] == shift.time_range
                )]
            
            if not self.assigned[day]:  
                del self.assigned[day]            

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
#    test = employees[emp].can_work('Friday', 'Afternoon', prev_day=None, prev_period=None)
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
        if employee not in self.assigned:
            self.assigned.append(employee)

    def unassign(self, employee):
        if employee in self.assigned:
            self.assigned.remove(employee)

    def __repr__(self):
        return f"Shift({self.period}, {self.time_range}, dept={self.department}, assigned={self.assigned})"
    



def shift_dictionary():    
    all_shifts = {}
    index_to_label = {}

    i = 0 
    for day in DAYS:
        daily_shifts_list = []
        for period, times in zip(PERIODS, [morning_required, afternoon_required, evening_required]):
            for time in times:
                shift = Shift(period, time, department_mapping[time], day)
                daily_shifts_list.append(shift)
                index_to_label[i] = (day, period, time, department_mapping[time])
                i += 1
                all_shifts[day] = daily_shifts_list

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
                  
      def backtracking(self):
          '''
          This method is in charge of assigning shifts
          If there is a conflict, the method will backtrack and schedule appropriately
          Checks if someone is assigned on that period, if not assign and mark rest of day off

          use can work method to see if someones available
          check shifts dictionary to find shift needing assigned
          build assign / unassign method
          build backtracker to check everything fits together
          '''
          least_assigned = self.least_assigned()

          ready_to_work = {}
 
          for day, periods_dict in least_assigned.items():
              ready_to_work[day] = {}
              for period, emp_list in periods_dict.items():
                  ready_to_work[day][period] = [
                      emp for emp in emp_list
                      if self.employees[emp].can_work(day, period, prev_day=None, prev_period=None)]
                  
          #schedule = {}

          #for day, shifts in all_shifts.items():   
          #    schedule[day] = []
    
          #    shifts_by_period = {}
          #    for shift in shifts:
          #        shifts_by_period.setdefault(shift.period, []).append(shift)
    
          #    for period, shifts_list in shifts_by_period.items():
          #        employees = ready_to_work.get(day, {}).get(period, [])
        
          #        for shift, emp in zip(shifts_list, employees):
          #            shift.assign(emp)  
          #            schedule[day].append((shift, emp))

          return ready_to_work
          

             
                    





rota = Scheduler(employees, all_shifts)
print(rota.backtracking())


# build backtracking into recent method in scheduler so it assigns correctly to the correct shift
# double check heuristics in can_work
