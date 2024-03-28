import random
from rest_framework import generics
from .models import Cargo, Vehicle, Location
from .serializers import CargoSerializer, VehicleSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from geopy.distance import distance
from rest_framework.decorators import action
import django_filters
from .filters import CargoFilter
from rest_framework import filters
from django.db.models import Q


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = CargoFilter
    search_fields = ['pick_up', 'delivery']

    def perform_create(self, serializer):
        pick_up = serializer.validated_data['pick_up']
        delivery = serializer.validated_data['delivery']
        serializer.save(pick_up=pick_up, delivery=delivery)

         
    

    def get_queryset(self):
        queryset = super().get_queryset()
        pick_up = self.request.query_params.get('pick_up', None)
        delivery = self.request.query_params.get('delivery', None)
        description = self.request.query_params.get('description', None)
        min_weight = self.request.query_params.get('min_weight', 0)
        max_weight = self.request.query_params.get('max_weight', 1000)

        if pick_up is not None:
            queryset = queryset.filter(pick_up__zip_code__icontains=pick_up)
        if delivery is not None:
            queryset = queryset.filter(delivery__zip_code__icontains=delivery)
        if description is not None:
            queryset = queryset.filter(description__icontains=description)
        queryset = queryset.filter(weight__gte=int(min_weight), weight__lte=int(max_weight))
        return queryset

    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = []
        for cargo in serializer.data:
            pick_up = cargo['pick_up']
            delivery = cargo['delivery']
            location_pick_up = Location.objects.get(pk=pick_up)
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


