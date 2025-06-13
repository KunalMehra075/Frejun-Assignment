from rest_framework import serializers
from .models import Team, Booking
from users.serializers import UserSerializer
from rooms.serializers import RoomSerializer
from users.models import User
from rooms.models import Room

class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'members']

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        team = Team.objects.create(**validated_data)
        for member_data in members_data:
            user, _ = User.objects.get_or_create(**member_data)
            team.members.add(user)
        return team

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'room', 'user', 'team', 'start_time', 'end_time', 'booking_type', 'status', 'created_at'] 