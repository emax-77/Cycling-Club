from time import timezone
from django.db import models

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.CharField(max_length=255, null=True)
  joined_date = models.DateField(null=True)
  address = models.CharField(max_length=255,null=True)
  zipcode = models.CharField(max_length=255,null=True)
  city = models.CharField(max_length=255,null=True)
  country = models.CharField(max_length=255,null=True)
  member_fees = models.IntegerField(null=True)

class Expenses(models.Model):
  member = models.ForeignKey(Member, on_delete=models.CASCADE)
  payment_date = models.DateField(null=True)
  event_name = models.CharField(max_length=255,null=True)
  purpose = models.CharField(max_length=255,null=True)
  amount = models.IntegerField(null=True)

class ClubEvents(models.Model):
  event_name = models.CharField(max_length=255, null=True)
  event_date = models.DateField(null=True)
  event_members = models.CharField(max_length=255, null=True)

class EventSubscribe(models.Model):
  name = models.CharField(max_length=100, null=True)
  email = models.EmailField(unique=True, max_length=100)
  event =  models.CharField(max_length=255, null=True)

class ClubPicture(models.Model): 
    name = models.CharField(max_length=255) 
    description = models.TextField() 
    image = models.ImageField(upload_to='products/') 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    

