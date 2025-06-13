from django.urls import path
from bookings.views import (
    BookingsView,
    BookingCancelView,
)

urlpatterns = [
    path('', BookingsView.as_view(), name='bookings'),
    path('cancel/<int:booking_id>', BookingCancelView.as_view(), name='booking-cancel'),
] 