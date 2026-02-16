from django.db import models
from django.conf import settings
from trips.models import Trip


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')

    seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    booking_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    selected_seats = models.TextField(blank=True)
    passenger_details = models.TextField(blank=True)

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f'{self.user.email} - {self.trip} ({self.seats} seat(s))'
