from rest_framework.views import APIView
from rest_framework.response import Response
from rooms.models import Room
from bookings.models import Booking
from rooms.serializers import RoomSerializer
from datetime import datetime

from django.utils.dateparse import parse_datetime
from roombooking.permissions import IsManagerOrAdmin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class GetRoomsView(APIView):
    """
    API endpoint to retrieve all currently booked rooms.
    
    This endpoint returns a list of all rooms that are currently occupied at the present time.
    Only accessible by managers and administrators.
    
    Returns:
        Response: A list of room objects with their details including:
            - room_number
            - room_type (PRIVATE/CONFERENCE/SHARED)
            - capacity
            - status
    """
    permission_classes = [IsManagerOrAdmin]
    
    def get(self, request):
        current_time = datetime.now()
        
 
        active_bookings = Booking.objects.filter(
            start_time__lte=current_time,
            end_time__gte=current_time,
            status="ACTIVE"
        )
        
        booked_rooms = Room.objects.filter(
            id__in=active_bookings.values_list('room_id', flat=True)
        )
        
        serializer = RoomSerializer(booked_rooms, many=True)
        return Response(serializer.data)




@method_decorator(csrf_exempt, name='dispatch')
class RoomAvailabilityView(APIView):
    """
    API endpoint to check room availability for a specific time slot and room type.
    
    Query Parameters:
        room_type (str): Type of room to check (PRIVATE/CONFERENCE/SHARED)
        slot (str): ISO 8601 formatted datetime string (YYYY-MM-DDTHH:MM)
    
    Returns:
        Response: A list of available rooms matching the criteria, including:
            - room_number
            - room_type
            - capacity
            - status
    
    Error Responses:
        - 400: Invalid room type or slot format
        - 400: Slot is in the past
        - 400: Slot is outside business hours (9am-6pm)
    """
  
    def get(self, request):
        room_type = request.query_params.get('room_type')
        slot = request.query_params.get('slot')
        
        
        start_time = parse_datetime(slot) if slot else None
        
      
        if room_type not in ["PRIVATE", "CONFERENCE", "SHARED"]:
            return Response({"error": "Invalid room type. Must be one of: PRIVATE, CONFERENCE, SHARED"}, status=400)
        
    
        if not start_time or not isinstance(start_time, datetime):
            return Response({"error": "Invalid slot format. Use ISO 8601."}, status=400)
        
 
        if start_time < datetime.now():
            return Response({"error": "Slot is in the past."}, status=400)
        
        if start_time.hour < 9 or start_time.hour > 18:
            return Response({"error": "Slot is not between 9am and 6pm."}, status=400)
        

        
        room_type = room_type.upper()
        available_rooms = []
        for room in Room.objects.filter(room_type=room_type):
            if room_type == "SHARED":
                current_bookings = Booking.objects.filter(room=room, start_time=start_time, status="ACTIVE").count()
                if current_bookings < room.capacity:
                    available_rooms.append(room)
            else:
                if not Booking.objects.filter(room=room, start_time=start_time, status="ACTIVE").exists():
                    available_rooms.append(room)
        serializer = RoomSerializer(available_rooms, many=True)
        return Response(serializer.data)
