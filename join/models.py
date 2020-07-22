from django.db import models
from datetime import date
from datetime import time
from datetime import datetime
from django.db.models.signals import post_save
from django.conf import settings


   
# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    psw=models.CharField(max_length=100)

    

    

class Userinformation(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    username=User.name
    image=models.ImageField(default='pp.jpg',upload_to='images')
    calculation_history=models.TextField()
    calculation_water=models.TextField()
    calculation_coffee=models.TextField()
    calculation_exercise=models.TextField()
    posted_date = models.DateField(default=date.today)

    def __str__(self):
        return  self.user.name





class Data(models.Model):
    exercise=models.CharField(max_length=500)
    amount=models.IntegerField(default=0)

    def __str__(self):
        return self.exercise




    
    


