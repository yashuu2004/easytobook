from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from bookings.models import Booking
from .models import Payment
import razorpay


@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.is_paid:
        return redirect('accounts:dashboard')

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    order = client.order.create({
        "amount": int(booking.total_price * 100),  # convert to paise
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        "booking": booking,
        "razorpay_order_id": order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    }

    return render(request, "payments/payment.html", context)


@login_required
def payment_success_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    booking.is_paid = True
    booking.save()

    Payment.objects.get_or_create(
        booking=booking,
        defaults={
            "amount": booking.total_price,
            "transaction_id": "RAZORPAY_SUCCESS"
        }
    )

    return render(request, "payments/success.html", {"booking": booking})


def payment_success(request):
    return render(request, 'payments/success.html')