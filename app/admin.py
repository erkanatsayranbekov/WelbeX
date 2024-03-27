from django.contrib import admin
from .models import Cargo, Location, Vehicle

admin.site.register(Cargo)
admin.site.register(Vehicle)
admin.site.register(Location)
