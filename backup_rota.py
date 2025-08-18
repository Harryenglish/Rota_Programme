import pandas as pd


# any magic numbers must be declared 

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

# Now we need a way of classifying every employee and their availability 

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

      

print(employees)


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

morning_shifts, afternoon_shifts, evening_shifts = shift_classifier()

# test = print(shift_classifier())


# Schedular class


class Scheduler:
      '''
      Classify which shifts are morning, afternoon and evening. 
      Check least available shifts to most, and assign accordingly.
      No shifts twice and maximum one a day.
      Show which shifts havent been taken.
      Show whos available but havent been assigned.
      
      
      Ultimately a constraint satisfaction problem. Backtracking with Heuristics.
      '''

      morning_required = ["7:00 - 13:00", "10:00 - 18:00", "8:00 - 13:00", "9:00 - 17:00"]
      afternoon_required = ["16:00 - 00:00", "12:00 - 22:00", "14:00 - 23:00"]
      evening_required = ["17:00 - 01:00", "17:00 - 00:00"]


      def __init__(self, morning_shifts, afternoon_shifts, evening_shifts):
        self.morning_shifts = morning_shifts
        self.afternoon_shifts = afternoon_shifts
        self.evening_shifts = evening_shifts
        self.assigned = []

      def Scheduling(self, morning_shifts, afternoon_shifts, evening_shifts, morning_required, afternoon_required, evening_required):
        '''
        For each day tally morning, afternoon and evening availability
        Assign shifts from least to most availability
        Do this for every day
        First come first serve basis

        Show which shifts arent filled
        Maximum one shift per day
        One shift given out once
        '''
        all_assigned = []

        for j in range(7):

            all_assigned.append(f"Day {j + 1}")

            for i in range(len(df['Name'])):
                morning_tally = 0
                afternoon_tally = 0
                evening_tally = 0
                if morning_shifts[i][1][j] == True:
                    morning_tally += 1
                if afternoon_shifts[i][1][j] == True:
                    afternoon_tally += 1
                if evening_shifts[i][1][j] == True:
                    evening_tally += 1

            tallies = [(morning_shifts, morning_tally, morning_required),
                       (afternoon_shifts, afternoon_tally, afternoon_required),
                       (evening_shifts, evening_tally, evening_required)]

            sorted_tallies = sorted(tallies, key=lambda x: x[1])

            (min_var, min_val, most_important_period), (mid_var, mid_val, middle_important_period), (max_var, max_val, least_important_period) = sorted_tallies

            # find which period it is, assign shifts in ascending order, get list of who can do shift in that period, assign max one
            assigned = []

            # make a function for most important period, pass in min_val, and use important_period as variable, same for middle and most  

            for i in range(len(df['Name'])):
            
                def highest_priority_period(min_var):
            
                    available_employees = []
                    # loop through morning shifts and acquire the name for what index is true
                    if min_var[i][1][j] == True:
                        available_employees.append(min_var[i][0])

                    if len(available_employees) < len(most_important_period):
                        available_employees.extend(["N/A"] * (len(most_important_period) - len(available_employees)))

                    assigned_for_this_period = list(zip(available_employees[:len(most_important_period)], most_important_period))
                    assigned.extend(assigned_for_this_period)

                    for emp, shift in assigned_for_this_period:
                        if emp == "N/A":
                            print(f"On day {j+1} the shift {shift} has nobody to take it.")    
                
                #assigned.append((available_employees[:len(most_important_period)], most_important_period))

                #for k in range(len(most_important_period)):
                #   if assigned[k][0] == "N/A":
                #        print(f"On day {j} the shift {assigned[k][1]} has nobody to take it.")

                    if min_var[i][1][j] == True:                    
                        min_var[i][1][j] = False
                        mid_var[i][1][j] = False 
                        max_var[i][1][j] = False

                    return assigned
            
                all_assigned.append(highest_priority_period(min_var))
            
                def middle_priority_period(mid_var):

                    available_employees = []

                    if mid_var[i][1][j] == True:
                        available_employees.append(mid_var[i][0])

                    if len(available_employees) < len(middle_important_period):
                        available_employees.extend(["N/A"] * (len(middle_important_period) - len(available_employees)))

                    assigned_for_this_period = list(zip(available_employees[:len(middle_important_period)], middle_important_period))
                    assigned.extend(assigned_for_this_period)

                    for emp, shift in assigned_for_this_period:
                        if emp == "N/A":
                            print(f"On day {j+1} the shift {shift} has nobody to take it.")    

                #assigned.append((available_employees[:len(middle_important_period)], middle_important_period))

                #for k in range(len(middle_important_period)):
                #    if assigned[k][0] == "N/A":
                #        print(f"On day {j} the shift {assigned[k][1]} has nobody to take it.")

                    if mid_var[i][1][j] == True:
                        mid_var[i][1][j] = False
                        max_var[i][1][j] = False
               
                    return assigned
            
                all_assigned.append(middle_priority_period(mid_var))    

                def least_priority_period(max_var):

                    available_employees = []

                    if max_var[i][1][j] == True:
                        available_employees.append(max_var[i][0])

                    if len(available_employees) < len(least_important_period):
                        available_employees.extend(["N/A"] * (len(least_important_period) - len(available_employees)))

                    assigned_for_this_period = list(zip(available_employees[:len(least_important_period)], least_important_period))
                    assigned.extend(assigned_for_this_period)

                    for emp, shift in assigned_for_this_period:
                        if emp == "N/A":
                            print(f"On day {j+1} the shift {shift} has nobody to take it.")      

                #assigned.append((available_employees[:len(least_important_period)], least_important_period))

                #for k in range(len(least_important_period)):
                #    if assigned[k][0] == "N/A":
                #        print(f"On day {j} the shift {assigned[k][1]} has nobody to take it.")

                    if max_var[i][1][j] == True:
                        max_var[i][1][j] = False

                    free_employees = []
                    if min_var[i][1][j] == True:
                        free_employees.append((min_var[i][0], "Highest priority period"))
                    if mid_var[i][1][j] == True:
                        free_employees.append((mid_var[i][0], "Middle priority period"))
                    if max_var[i][1][j] == True:
                        free_employees.append((max_var[i][0], "Lowest priority period"))
                    
                    if free_employees != 0:
                        print(f"The employees that have not been assigned shifts are {free_employees}")
    
                    return assigned 
            
                all_assigned.append(least_priority_period(max_var))
                 
            return all_assigned  # assigned is a schedular for one day, done for all 7
      
      def Exporter(self, all_assigned):
          '''
          This method will be in charge of exporting the rota into a viewable format

          Assign shift times to department
          '''
          rota = []

          for i in range(len(df['Name'])):     #  figure out how assigned list is structured and map to department
              if assigned[i][1] == "10:00 - 18:00":
                  assigned[i].append("W Lounge")
              elif assigned[i][1] == "12:00 - 22:00":
                  assigned[i].append("W Lounge")
              elif assigned[i][1] == "14:00 - 23:00":
                  assigned[i].append("W Lounge")
              elif assigned[i][1] == "17:00 - 01:00":
                  assigned[i].append("W Lounge")
              else:
                  assigned[i].append("Sushisamba")
                  # add assigned shifts and department to rota list, then make spredsheet from rota list  
              
          
          return rota
        



apparatus = Scheduler(morning_shifts, afternoon_shifts, evening_shifts)


# print(assigned)


#assigned = apparatus.Scheduling(morning_shifts, afternoon_shifts, evening_shifts, 
#                                 Scheduler.morning_required, Scheduler.afternoon_required, Scheduler.evening_required)

# print(assigned)
