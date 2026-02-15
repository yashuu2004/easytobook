from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('transport_type', 'source_city', 'destination_city', 'date', 'time', 'available_seats', 'price')
    list_filter = ('transport_type', 'date')
    search_fields = ('source_city__name', 'destination_city__name')
    date_hierarchy = 'date'
