from django_filters import rest_framework as filters
from .models import Cargo

class CargoFilter(filters.FilterSet):
    min_weight = filters.NumberFilter(field_name="weight", lookup_expr='gte')
    max_weight = filters.NumberFilter(field_name="weight", lookup_expr='lte')

    class Meta:
        model = Cargo
        fields = ['min_weight', 'max_weight', 'description']