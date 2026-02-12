from django.db import models

from Adminapp.models import Location


class Login(models.Model):
    objects=None
    Loginid=models.AutoField(primary_key=True)
    Username=models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Role= models.CharField(max_length=15)
    Status = models.CharField(max_length=15)

class Author(models.Model):
    objects=None
    Authorid=models.AutoField(primary_key=True)
    Authorname=models.CharField(max_length=50)
    Authorcontact=models.BigIntegerField()
    Authoremail=models.CharField(max_length=50)
    Authoraddress=models.CharField(max_length=50)
    Authorimg=models.ImageField()
    Regdate=models.DateField(auto_now_add=True)
    Loginid=models.ForeignKey(Login,on_delete=models.CASCADE)

class User(models.Model):
    objects=None
    Userid=models.AutoField(primary_key=True)
    UserName=models.CharField(max_length=50)
    Usercontact=models.BigIntegerField()
    Useremail=models.CharField(max_length=50)
    UserRegdate=models.DateField(auto_now_add=True)
    Locationid=models.ForeignKey(Location,on_delete=models.CASCADE,default=None)
    Loginid=models.ForeignKey(Login,on_delete=models.CASCADE,default=None)
    
