

from django.urls import path
from rooms.views import GetRoomsView,RoomAvailabilityView


urlpatterns = [
    path('', GetRoomsView.as_view(), name='booked-rooms'),
    path('available', RoomAvailabilityView.as_view(), name='room-availability'),
]
