from django.core.management.base import BaseCommand
from datetime import date, timedelta, time
from decimal import Decimal
from trips.models import Trip
from locations.models import City


class Command(BaseCommand):
    help = "Generate demo trips"

    def handle(self, *args, **kwargs):

        cities = list(City.objects.all())

        if len(cities) < 2:
            self.stdout.write("Need at least 2 cities")
            return

        source_city = cities[0]
        dest_city = cities[1]

        for i in range(7):
            trip_date = date.today() + timedelta(days=i)

            Trip.objects.get_or_create(
                transport_type="BUS",
                source_city=source_city,
                destination_city=dest_city,
                date=trip_date,
                time=time(10, 0),
                defaults={
                    "price": Decimal("499"),
                    "available_seats": 40
                }
            )

        self.stdout.write(self.style.SUCCESS("Trips generated"))
