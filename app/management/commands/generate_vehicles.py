import random
import string
from django.core.management.base import BaseCommand, CommandError
from app.models import Location, Vehicle

class Command(BaseCommand):
    help = 'Generate and add a specified number of vehicles to the database'

    def add_arguments(self, parser):
        parser.add_argument('num_vehicles', type=int, nargs='?', default=20, help='Number of vehicles to generate (default is 20)')

    def handle(self, *args, **options):
        num_vehicles = options['num_vehicles']

        locations = Location.objects.all()

        if len(locations) < num_vehicles:
            raise CommandError('Not enough locations available to generate vehicles.')

        for _ in range(num_vehicles):
            location = random.choice(locations)
            unique_number = ''.join(random.choices(string.digits, k=4)) + random.choice(string.ascii_uppercase)

            carrying_capacity = random.randint(1, 1000)

            Vehicle.objects.create(
                unique_number=unique_number,
                current_location=location,
                carrying_capacity=carrying_capacity,
            )

        self.stdout.write(self.style.SUCCESS(f'{num_vehicles} vehicles generated and added to the database'))
