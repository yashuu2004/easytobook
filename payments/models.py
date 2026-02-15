from django.db import models
from django.conf import settings
from bookings.models import Booking


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    # Simulated gateway reference
    transaction_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Payment for Booking #{self.booking.id}'
