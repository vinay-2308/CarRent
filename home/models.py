from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User
from django.utils.html import mark_safe

class Location(models.Model): #Stores city names where cars and users are located.
    city = models.CharField(max_length = 50)

    def _str_(self):
        return self.city

class CarDealer(models.Model):
    car_dealer = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(validators = [MinLengthValidator(10), MaxLengthValidator(10)], max_length = 10)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    earnings = models.IntegerField(default = 0)
    type = models.CharField(max_length = 20, blank = True)

    def __str__(self):
        return str(self.car_dealer)

class Car(models.Model): #Represents each car available for rent.
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="")
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.PROTECT)
    capacity = models.CharField(max_length=2)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    is_available = models.BooleanField(default=True)
    rent = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name
    
    def img_preview(self): #new
        return mark_safe(f'<img src = "{self.image.url}" width = "100"/>')

class Customer(models.Model): # adds extra fields and logic specific to customers on top of Django’s built-in User.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(validators = [MinLengthValidator(10), MaxLengthValidator(10)], max_length = 10)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    type  = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(self.user)

class Order(models.Model): #Stores rental transactions.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rent = models.CharField(max_length=10)
    days = models.CharField(max_length=3)
    is_complete = models.BooleanField(default=False)
    
    

# Create your models here.
