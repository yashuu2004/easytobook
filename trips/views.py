from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .models import Trip
from locations.models import State


def home_view(request):
    return render(request, 'trips/home.html')


def trip_search_view(request):
    from locations.models import City
    states = State.objects.prefetch_related('cities').order_by('name')
    transport_type = request.GET.get('transport_type', '')
    source_id = request.GET.get('source_city', '')
    dest_id = request.GET.get('destination_city', '')
    date = request.GET.get('date', '')
    source_state_id = request.GET.get('source_state', '')
    dest_state_id = request.GET.get('dest_state', '')
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
    if transport_type and source_id and dest_id and date:
        trips = Trip.objects.filter(
            transport_type=transport_type,
            source_city_id=source_id,
            destination_city_id=dest_id,
            date=date,
            available_seats__gt=0
        ).select_related('source_city', 'destination_city', 'source_city__state', 'destination_city__state').order_by('time')
    context = {
        'states': states,
        'trips': trips,
        'transport_type': transport_type,
        'source_id': source_id,
        'dest_id': dest_id,
        'source_state_id': source_state_id,
        'dest_state_id': dest_state_id,
        'date': date,
    }
    return render(request, 'trips/search.html', context)


def trip_detail_view(request, pk):
    trip = get_object_or_404(Trip.objects.select_related('source_city', 'destination_city'), pk=pk)
    return render(request, 'trips/trip_detail.html', {'trip': trip})
