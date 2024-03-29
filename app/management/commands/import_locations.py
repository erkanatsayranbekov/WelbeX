import pandas as pd
from django.core.management.base import BaseCommand
from app.models import Location
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Import locations from uszips.csv'

    def handle(self, *args, **options):
        csv_file = os.path.join(settings.BASE_DIR, 'app/management/commands/uszips.csv')
        try:
            data = pd.read_csv(csv_file, encoding='utf-8',  dtype={'zip': str})
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File {csv_file} not found.'))
            return
        for index, row in data.iterrows():
            Location.objects.create(
                city=row['city'],
                state=row['state_id'],
                zip_code=row['zip'],
                latitude=float(row['lat']),
                longitude=float(row['lng']),
            )

        self.stdout.write(self.style.SUCCESS('Locations imported successfully'))
