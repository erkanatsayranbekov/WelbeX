from celery import shared_task
from celery.schedules import crontab
from .models import Location, Vehicle
import logging

logger = logging.getLogger(__name__)

@shared_task(run_every=crontab(minute="*/3"))
def update_vehicle_locations():
    try:
        random_location = Location.objects.order_by('?').first()
        if random_location:
            Vehicle.objects.update(current_location=random_location)
            logger.info(f"Updated vehicle locations with new random location: {random_location}")
        else:
            logger.warning("No locations found in the database.")
    except Exception as e:
        logger.error(f"Error updating vehicle locations: {e}")
