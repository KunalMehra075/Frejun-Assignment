from django.db import models

class User(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    ROLE_CHOICES = [
        ("user", "User"),
        ("admin", "Admin"),
        ("manager", "Manager"),
    ]
    
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True, blank=True) 
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")

    def __str__(self):
        return f"{self.name} ({self.age})"

