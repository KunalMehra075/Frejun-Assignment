from django.db import models
from users.models import User
from rooms.models import Room

class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="teams")

    def __str__(self):
        return self.name

class Booking(models.Model):
    BOOKING_TYPE_CHOICES = [
        ("INDIVIDUAL", "Individual"),
        ("TEAM", "Team"),
    ]
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
    
        ("CANCELLED", "Cancelled"),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room} | {self.start_time} - {self.end_time}"
