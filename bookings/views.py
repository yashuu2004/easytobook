from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from trips.models import Trip
from .models import Booking


@login_required
def create_booking_view(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    if request.method != 'POST':
        return redirect('trips:trip_detail', pk=trip_id)
    seats = request.POST.get('seats')
    if not seats:
        messages.error(request, 'Please select number of seats.')
        return redirect('trips:trip_detail', pk=trip_id)
    try:
        seats = int(seats)
    except (TypeError, ValueError):
        messages.error(request, 'Invalid number of seats.')
        return redirect('trips:trip_detail', pk=trip_id)
    if seats < 1:
        messages.error(request, 'At least 1 seat is required.')
        return redirect('trips:trip_detail', pk=trip_id)
    with transaction.atomic():
        trip = Trip.objects.select_for_update().get(pk=trip_id)
        if trip.available_seats < seats:
            messages.error(request, f'Only {trip.available_seats} seat(s) available.')
            return redirect('trips:trip_detail', pk=trip_id)
        total_price = trip.price * seats
        booking = Booking.objects.create(
            user=request.user,
            trip=trip,
            seats=seats,
            total_price=total_price,
            is_paid=False,
        )
        trip.available_seats -= seats
        trip.save(update_fields=['available_seats'])
    return redirect('payments:payment', booking_id=booking.id)


def _send_booking_confirmation(booking):
    subject = f'Booking Confirmation - {booking.trip.get_transport_type_display()}'
    message = (
        f'Hi {booking.user.get_full_name() or booking.user.email},\n\n'
        f'Your booking is confirmed.\n\n'
        f'Trip: {booking.trip.get_transport_type_display()} from {booking.trip.source_city} to {booking.trip.destination_city}\n'
        f'Date: {booking.trip.date} at {booking.trip.time}\n'
        f'Seats: {booking.seats}\n'
        f'Total: ₹{booking.total_price}\n\n'
        f'Thank you for choosing HBooking!'
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        fail_silently=False,
    )
