from django.urls import include, path
from .views import CargoViewSet, VehicleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cargos', CargoViewSet)
router.register('vehicles', VehicleViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
