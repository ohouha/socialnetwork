from django.db import models
import datetime

# Create your models here.

# User class for built-in authentication module
from django.contrib.auth.models import User


class profile(models.Model):
    firstname=models.CharField(max_length=50) #mention>50
    lastname=models.CharField(max_length=50)
    username= models.CharField(max_length=200,blank=True)
    user = models.ForeignKey(User)
    age=models.CharField(max_length=5) #limit here
    short_bio=models.CharField(max_length=200) #limit here
    picture=models.ImageField(upload_to="socialnetwork-photo",blank=True)
    def __str__(self):    #python 3->need to change
        return self.firstname

class Item(models.Model):
    message = models.CharField(max_length=200)
    username= models.CharField(max_length=200)
    #user = models.ForeignKey(User)
    #date=models.DateTimeField(auto_now_add=True,blank=True)
    date=models.DateTimeField()
    user =models.ForeignKey(profile, on_delete=models.CASCADE,default=None, blank=True, null=True,db_column='image')
    def __str__(self):    #python 3->need to change
        return self.message


class Person(models.Model):
    user = models.ForeignKey(User)
    username = models.CharField(max_length=100)
    otherpeople=models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.otherpeople

class Comments(models.Model):
    content = models.CharField(max_length=200)
    username= models.CharField(max_length=200)
    date=models.DateTimeField()
    post =models.ForeignKey(Item, on_delete=models.CASCADE,default=None, blank=True, null=True,db_column='post',related_name='views')
    mypro =models.ForeignKey(profile, on_delete=models.CASCADE,default=None, blank=True, null=True,db_column='pro',related_name='profiles')
    def __str__(self):    #python 3->need to change
        return self.username
