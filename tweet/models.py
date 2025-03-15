from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime




class Tweet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField(max_length=240)
    photo=models.ImageField(upload_to="photos/",blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}-{self.text[:10]}'
    
class Residents(models.Model):
    CATEGORY_CHOICES = [
        ('Resident', 'Resident'),
        ('Visitor', 'Visitor'),
        ('Criminal', 'Criminal'),
    ]

    owner_name = models.CharField(max_length=100,default='Unknown')
    vehicle_number = models.CharField(max_length=20, unique=True)
    resident_address = models.TextField(default="Not Provided")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES,default='Resident')
    registered_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.vehicle_number} - {self.owner_name}"

class Logbook(models.Model):
    CATEGORY_CHOICES = [
        ('Resident', 'Resident'),
        ('Visitor', 'Visitor'),
        ('Criminal', 'Criminal'),
    ]

    owner_name = models.CharField(max_length=100,default='Unknown')
    vehicle_number = models.CharField(max_length=20)
    resident_address = models.TextField(default="Not Provided")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES,default='Resident')
    registered_date = models.DateField(auto_now_add=True)  
    registered_time = models.TimeField(auto_now_add=True)

