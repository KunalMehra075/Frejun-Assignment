from django.db import models

# Create your models here.

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ("PRIVATE", "Private Room"),
        ("CONFERENCE", "Conference Room"),
        ("SHARED", "Shared Desk"),
    ]
    room_type = models.CharField(max_length=15, choices=ROOM_TYPE_CHOICES)
    capacity = models.PositiveIntegerField()
    room_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.room_type} - {self.room_number}"
