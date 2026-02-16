from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:trip_id>/', views.create_booking_view, name='create'),
    path('ticket/<int:booking_id>/', views.ticket_view, name='ticket'),
]

