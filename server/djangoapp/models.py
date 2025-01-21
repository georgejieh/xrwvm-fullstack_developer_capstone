from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# CarMake model
class CarMake(models.Model):
    name = models.CharField(max_length=100)  # Name of the car make
    description = models.TextField()  # Description of the car make

    def __str__(self):
        return self.name  # Return the name of the car make as a string representation


# CarModel model
class CarModel(models.Model):
    car_make = models.ForeignKey(
        CarMake, 
        on_delete=models.CASCADE
    )  # Many-to-One relationship
    dealer_id = models.IntegerField(
        null=True, 
        blank=True, 
        default=0
    )  # Optional with default value
    name = models.CharField(max_length=100)  # Name of the car model
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    type = models.CharField(
        max_length=20, 
        choices=CAR_TYPES, 
        default='SEDAN'
    )  # Type of the car model
    year = models.IntegerField(  # Store the year as an integer
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015),
        ]
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
