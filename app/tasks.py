import random
from celery import shared_task
from .models import Vehicle, Location

@shared_task()
def update_database_task():
    vehicles = Vehicle.objects.all()
    for vehicle in vehicles:
        locations = Location.objects.exclude(pk=vehicle.current_location.pk)
        new_location = random.choice(locations)
        vehicle.current_location = new_location
        vehicle.save()



