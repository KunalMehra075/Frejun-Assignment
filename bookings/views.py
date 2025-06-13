from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking
from rooms.models import Room
from users.models import User
from .serializers import BookingSerializer, TeamSerializer
from users.serializers import UserSerializer
from django.utils.dateparse import parse_datetime
from django.db import transaction
from datetime import  timedelta

from roombooking.utils import StandardResultsSetPagination
from roombooking.permissions import IsManagerOrAdmin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class BookingsView(APIView):
    """
    API endpoint for managing room bookings.
    
    This endpoint handles both individual and team bookings for different types of rooms.
    Only accessible by managers and administrators.
    
    Methods:
        GET: Retrieve all bookings (with optional status filter)
        POST: Create a new booking
    
    GET Query Parameters:
        status (str, optional): Filter bookings by status (e.g., 'cancelled')
    
    POST Request Body:
        {
            "user": {
                "name": str,
                "age": int,
                "gender": str
            } OR
            "team": {
                "name": str,
                "members": [
                    {
                        "name": str,
                        "age": int,
                        "gender": str
                    }
                ]
            },
            "room_type": str,  # One of: "PRIVATE", "CONFERENCE", "SHARED"
            "slot": str  # ISO 8601 format (YYYY-MM-DDTHH:MM)
        }
    
    Returns:
        GET: Paginated list of bookings
        POST: Created booking details with booking_id and room number
    
    Error Responses:
        - 400: Invalid request data
        - 400: Room type restrictions not met
        - 400: No available rooms
        - 400: User/team member already has a booking
        - 400: Conference room requires minimum 3 team members
    """
    permission_classes = [IsManagerOrAdmin]
    pagination_class = StandardResultsSetPagination
    
    def get(self, request):
        if request.query_params.get('status') == 'cancelled':
            queryset = Booking.objects.filter(status='CANCELLED').order_by('-created_at')
        else:
            queryset = Booking.objects.all().order_by('-created_at')
       
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = BookingSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    
    @transaction.atomic
    def post(self, request):
        data = request.data
        
        room_type = data.get("room_type")
        slot = data.get("slot")
   
        if room_type not in ["PRIVATE", "CONFERENCE", "SHARED"]:
            return Response({"error": "Invalid room type. Must be one of: PRIVATE, CONFERENCE, SHARED"}, status=400)
        if not slot or not isinstance(slot, str):
            return Response({"error": "Slot is invalid, must be a string in the format YYYY-MM-DDTHH:MM."}, status=400)
        
        
        start_time = parse_datetime(slot)
        if not start_time:
            return Response({"error": "Invalid slot format. Use ISO 8601."}, status=400)
        end_time = start_time + timedelta(hours=1)

     
        user_data = data.get("user")
        team_data = data.get("team")
        booking_type = None
        user = None
        team = None
        headcount = 0
        

        if user_data:
            booking_type = "INDIVIDUAL"
            user_serializer = UserSerializer(data=user_data)
            if not user_serializer.is_valid():
                return Response({"error": "Invalid user data.", "details": user_serializer.errors}, status=400)

            validated_data = user_serializer.validated_data
            user,_ = User.objects.get_or_create(
                name=validated_data['name'],
                defaults={
                    'age': validated_data['age'],
                    'gender': validated_data.get('gender')
                }
            )

      
            if Booking.objects.filter(user=user, start_time=start_time, status="ACTIVE").exists():
                return Response({"error": "User already has a booking in this slot."}, status=400)
            headcount = 1 if user.age >= 10 else 0
        elif team_data:
            booking_type = "TEAM"
            team_serializer = TeamSerializer(data=team_data)
            if not team_serializer.is_valid():
                return Response({"error": "Invalid team data.", "details": team_serializer.errors}, status=400)
            team = team_serializer.save()
    
            for member in team.members.all():
                if Booking.objects.filter(user=member, start_time=start_time, status="ACTIVE").exists():
                    return Response({"error": f"Team member {member.name} already has a booking in this slot."}, status=400)

            headcount = sum(1 for m in team.members.all() if m.age >= 10)
            if headcount < 3 and room_type == "CONFERENCE":
                return Response({"error": "Conference rooms require at least 3 team members (excluding children)."}, status=400)
        else:
            return Response({"error": "Must provide either user or team."}, status=400)

   
        available_room = None
        if room_type == "PRIVATE":
            if booking_type != "INDIVIDUAL":
                return Response({"error": "Private rooms can only be booked by individuals."}, status=400)
      
            for room in Room.objects.filter(room_type="PRIVATE"):
                if not Booking.objects.filter(room=room, start_time=start_time, status="ACTIVE").exists():
                    available_room = room
                    break
        elif room_type == "CONFERENCE":
            if booking_type != "TEAM":
                return Response({"error": "Conference rooms can only be booked by teams."}, status=400)
            for room in Room.objects.filter(room_type="CONFERENCE"):
                if not Booking.objects.filter(room=room, start_time=start_time, status="ACTIVE").exists():
                    available_room = room
                    break
        elif room_type == "SHARED":
            if booking_type != "INDIVIDUAL":
                return Response({"error": "Shared desks can only be booked by individuals."}, status=400)
     
            for room in Room.objects.filter(room_type="SHARED"):
             
                current_bookings = Booking.objects.filter(room=room, start_time=start_time, status="ACTIVE").count()
                if current_bookings < room.capacity:
                    available_room = room
                    break
        else:
            return Response({"error": "Invalid room type."}, status=400)

        if not available_room:
            return Response({"error": "No available room for the selected slot and type."}, status=400)

  
        booking = Booking.objects.create(
            room=available_room,
            user=user,
            team=team,
            start_time=start_time,
            end_time=end_time,
            booking_type=booking_type,
            status="ACTIVE"
        )
        return Response({"booking_id": booking.id, "room": available_room.room_number}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class BookingCancelView(APIView):
    """
    API endpoint to cancel an active booking.
    
    URL Parameters:
        booking_id (int): The ID of the booking to cancel
    
    Returns:
        Response: Success message if booking is cancelled
    
    Error Responses:
        - 404: Booking not found or already cancelled
    """
    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, status="ACTIVE")
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found or already cancelled."}, status=404)
        booking.status = "CANCELLED"
        booking.save()
        return Response({"message": "Booking cancelled successfully."}, status=200)

 