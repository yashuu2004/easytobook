from django.core.management.base import BaseCommand
from locations.models import State, City
from trips.models import Trip
from datetime import date, time, timedelta


class Command(BaseCommand):
    help = 'Load sample states, cities, and trips for testing.'

    def handle(self, *args, **options):
        State.objects.all().delete()
        s1, _ = State.objects.get_or_create(name='Maharashtra')
        s2, _ = State.objects.get_or_create(name='Karnataka')
        s3, _ = State.objects.get_or_create(name='Tamil Nadu')
        City.objects.filter(state=s1).delete()
        City.objects.filter(state=s2).delete()
        City.objects.filter(state=s3).delete()
        c1, _ = City.objects.get_or_create(state=s1, name='Mumbai')
        c2, _ = City.objects.get_or_create(state=s1, name='Pune')
        c3, _ = City.objects.get_or_create(state=s2, name='Bengaluru')
        c4, _ = City.objects.get_or_create(state=s2, name='Mysuru')
        c5, _ = City.objects.get_or_create(state=s3, name='Chennai')
        c6, _ = City.objects.get_or_create(state=s3, name='Coimbatore')
        self.stdout.write('States and cities created.')

        Trip.objects.all().delete()
        d = date.today() + timedelta(days=1)
        for ttype in ['bus', 'train', 'flight']:
            Trip.objects.create(
                transport_type=ttype,
                source_city=c1,
                destination_city=c3,
                date=d,
                time=time(9, 0),
                total_seats=40,
                available_seats=40,
                price=500 if ttype == 'bus' else (800 if ttype == 'train' else 3500),
            )
            Trip.objects.create(
                transport_type=ttype,
                source_city=c2,
                destination_city=c3,
                date=d,
                time=time(14, 30),
                total_seats=35,
                available_seats=35,
                price=450 if ttype == 'bus' else (700 if ttype == 'train' else 3200),
            )
        self.stdout.write(self.style.SUCCESS('Sample trips created. Use Search with Maharashtra/Karnataka and tomorrow\'s date.'))
