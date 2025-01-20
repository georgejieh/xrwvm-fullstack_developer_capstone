from django.db import models

# CarMake model
class CarMake(models.Model):
    name = models.CharField(max_length=100)  # Name of the car make
    description = models.TextField()  # Description of the car make

    def __str__(self):
        return self.name  # Return the name of the car make as a string representation


# CarModel model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Many-to-One relationship
    dealer_id = models.IntegerField()  # Refers to a dealer created in Cloudant database
    name = models.CharField(max_length=100)  # Name of the car model
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    type = models.CharField(max_length=20, choices=CAR_TYPES, default='SEDAN')  # Type of the car model
    year = models.DateField()  # Year of the car model

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.type})"  # String representation
