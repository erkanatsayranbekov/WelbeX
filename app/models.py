from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import random
import string

class Location(models.Model):
    zip_code = models.CharField(primary_key=True, max_length=10)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.city}, {self.state} ({self.zip_code})"

class Cargo(models.Model):
    pick_up = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pick_up_cargo')
    delivery = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='delivery_cargo')
    weight = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    description = models.TextField()

    def __str__(self):
        return f"Cargo from {self.pick_up} to {self.delivery}"

class Vehicle(models.Model):
    def generate_unique_code():
        return str(random.randint(1000, 9999)) + random.choice(string.ascii_uppercase)

    unique_number = models.CharField(max_length=5, default=generate_unique_code, unique=True)
    current_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='vehicles')
    carrying_capacity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000)])

    def __str__(self):
        return f"Vehicle {self.unique_number} at {self.current_location}"
