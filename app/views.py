import random
from rest_framework import generics
from .models import Cargo, Vehicle, Location
from .serializers import CargoSerializer, VehicleSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from geopy.distance import distance
from rest_framework.decorators import action

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    def perform_create(self, serializer):
        pick_up = serializer.validated_data['pick_up']
        delivery = serializer.validated_data['delivery']
        serializer.save(pick_up=pick_up, delivery=delivery)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = []
        for cargo in serializer.data:
            pick_up = cargo['pick_up']
            delivery = cargo['delivery']
            location_pick_up = Location.objects.get(pk=pick_up)
            location_delivery = Location.objects.get(pk=delivery)
            vehicles = Vehicle.objects.filter(current_location=location_pick_up)
            vehicles_in_range = []
            for vehicle in vehicles:
                distance_to_vehicle = distance(
                    (location_pick_up.latitude, location_pick_up.longitude),
                    (vehicle.current_location.latitude, vehicle.current_location.longitude)).miles
                if distance_to_vehicle <= 450:
                    vehicles_in_range.append(vehicle.id)
            cargo['number_of_vehicles_in_range'] = len(vehicles_in_range)
            data.append(cargo)
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        cargo: Cargo = self.get_object()
        location_pick_up = cargo.pick_up
        vehicles = Vehicle.objects.all()
        data = CargoSerializer(cargo).data
        vehicles_in_range = []
        for vehicle in vehicles:
            distance_to_vehicle = distance(
                (location_pick_up.latitude, location_pick_up.longitude),
                (vehicle.current_location.latitude, vehicle.current_location.longitude)).miles
            if distance_to_vehicle <= 450:
                vehicles_in_range.append(vehicle.unique_number)
        data['vehicles_in_range'] = vehicles_in_range
        return Response(data)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer     


