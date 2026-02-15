from django.db import models
from locations.models import City


TRANSPORT_CHOICES = [
    ('bus', 'Bus'),
    ('train', 'Train'),
    ('flight', 'Flight'),
]


class Trip(models.Model):
    transport_type = models.CharField(max_length=20, choices=TRANSPORT_CHOICES)
    source_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='trips_from')
    destination_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='trips_to')
    date = models.DateField()
    time = models.TimeField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f'{self.get_transport_type_display()} {self.source_city} → {self.destination_city} ({self.date})'
