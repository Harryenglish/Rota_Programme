# Schematic for OOP rota programme

# Have a class for, employee, shifts, schedular, rota exporter, constraint checker

# Assign maximum shifts and none twice, assigning shifts to all departments with staff availability 


class Car:
    def __init__(self, brand, name):
        self.brand = brand
        self.name = name
        self.velocity = 0

    def accelerate(self):
        self.velocity = 0
        for i in range(10):
            self.velocity += i

    def status(self):
        print(f"The {self.brand} {self.name} is going at {self.velocity}")

my_car = Car("Bugatti", "Veyron")
my_car.accelerate()
my_car.status()

my_car.accelerate()
my_car.status()