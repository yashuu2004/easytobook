import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from bookings.models import Booking
from bookings.views import _send_booking_confirmation
from .models import Payment


@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related('trip'),
        id=booking_id,
        user=request.user,
    )
    if booking.is_paid:
        messages.success(request, 'This booking is already paid.')
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        # Simulate payment success (e.g. user clicked "Pay Now")
        with transaction.atomic():
            booking = Booking.objects.select_for_update().get(id=booking_id, user=request.user)
            if booking.is_paid:
                return redirect('accounts:dashboard')
            Payment.objects.get_or_create(
                booking=booking,
                defaults={
                    'amount': booking.total_price,
                    'transaction_id': f'TXN-{uuid.uuid4().hex[:16].upper()}',
                }
            )
            booking.is_paid = True
            booking.save(update_fields=['is_paid'])
        _send_booking_confirmation(booking)
        return redirect('payments:success', booking_id=booking.id)
    return render(request, 'payments/payment.html', {'booking': booking})


@login_required
def payment_success_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if not booking.is_paid:
        return render(request, 'payments/success.html', {'booking': booking})
    return render(request, 'payments/success.html', {'booking': booking})
