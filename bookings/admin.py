from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip', 'seats', 'total_price', 'booking_date', 'is_paid')
    list_filter = ('is_paid', 'booking_date')
    search_fields = ('user__email',)
    date_hierarchy = 'booking_date'
