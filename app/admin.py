from django.contrib import admin
from .models import Cargo, Location, Vehicle
from unfold.admin import ModelAdmin


admin.site.register(Cargo)
admin.site.register(Vehicle)
admin.site.register(Location)
class CustomAdminClass(ModelAdmin):
    pass



