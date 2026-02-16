from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .models import Trip
from locations.models import State
from datetime import date, time
from decimal import Decimal
from bookings.models import Booking


def home_view(request):
    return render(request, 'trips/home.html')


def trip_search_view(request):
    from locations.models import City

    states = State.objects.prefetch_related('cities').order_by('name')

    transport_type = request.GET.get('transport_type', '')
    source_id = request.GET.get('source_city', '')
    dest_id = request.GET.get('destination_city', '')
    date_param = request.GET.get('date', '')
    source_state_id = request.GET.get('source_state', '')
    dest_state_id = request.GET.get('dest_state', '')

    # Restore state selection if missing
    if source_id and not source_state_id:
        try:
            c = City.objects.values_list('state_id', flat=True).get(pk=source_id)
            source_state_id = str(c)
        except City.DoesNotExist:
            pass

    if dest_id and not dest_state_id:
        try:
            c = City.objects.values_list('state_id', flat=True).get(pk=dest_id)
            dest_state_id = str(c)
        except City.DoesNotExist:
            pass

    trips = []

    if transport_type and source_id and dest_id and date_param:

        # Try fetching existing trips
        trips = Trip.objects.filter(
            transport_type=transport_type,
            source_city_id=source_id,
            destination_city_id=dest_id,
            date=date_param,
            available_seats__gt=0
        ).select_related(
            'source_city',
            'destination_city',
            'source_city__state',
            'destination_city__state'
        ).order_by('time')

        # ⭐ Auto create demo trips if none found
        if not trips.exists():
            for hour in [8, 12, 16, 20]:
                Trip.objects.create(
                    transport_type=transport_type,
                    source_city_id=source_id,
                    destination_city_id=dest_id,
                    date=date_param,
                    time=time(hour, 0),
                    price=Decimal('499'),
                    total_seats=40,
                    available_seats=40
                )

            trips = Trip.objects.filter(
                transport_type=transport_type,
                source_city_id=source_id,
                destination_city_id=dest_id,
                date=date_param,
                available_seats__gt=0
            ).select_related(
                'source_city',
                'destination_city'
            ).order_by('time')

    context = {
        'states': states,
        'trips': trips,
        'transport_type': transport_type,
        'source_id': source_id,
        'dest_id': dest_id,
        'source_state_id': source_state_id,
        'dest_state_id': dest_state_id,
        'date': date_param,
    }

    return render(request, 'trips/search.html', context)

def trip_detail_view(request, pk):
    trip = get_object_or_404(
        Trip.objects.select_related('source_city', 'destination_city'),
        pk=pk
    )

    bookings = Booking.objects.filter(trip=trip)

    booked_seats = []
    for b in bookings:
        if b.selected_seats:
            booked_seats += b.selected_seats.split(",")

    # ⭐ Layout based on transport
    if trip.transport_type == "BUS":
        rows = list("ABCDE")
        seat_numbers = ["1", "2", "3", "4"]

    elif trip.transport_type == "TRAIN":
        rows = list("ABCDEFGHIJKL")  # 12 rows
        seat_numbers = ["1", "2", "3", "4", "5", "6"]  # sleeper style

    elif trip.transport_type == "FLIGHT":
        rows = list("ABCDEFGHIJKLMNOP")  # many rows
        seat_numbers = ["A", "B", "C", "D", "E", "F"]  # aircraft layout

    else:
        rows = list("ABCDE")
        seat_numbers = ["1", "2", "3", "4"]

    context = {
        "trip": trip,
        "booked_seats": booked_seats,
        "rows": rows,
        "seat_numbers": seat_numbers,
    }

    return render(request, "trips/trip_detail.html", context)
