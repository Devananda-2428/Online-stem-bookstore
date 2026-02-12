from django.db import models

class District(models.Model):
    DistrictId=models.AutoField(primary_key=True)
    DistrictName=models.CharField(max_length=50)


class Location(models.Model):
    objects=None
    Locationid=models.AutoField(primary_key=True)
    LocationName=models.CharField(max_length=50)
    DistrictId=models.ForeignKey(District,on_delete=models.CASCADE,default="")

class Tbl_Category(models.Model):
    objects = None
    Categoryid = models.AutoField(primary_key=True)
    Categoryname = models.CharField(max_length=50)
    Categoryimg = models.ImageField()

class Language(models.Model):
    objects=None
    Langid = models.AutoField(primary_key=True)
    LangName = models.CharField(max_length=25)

class Subcategory(models.Model):
    objects=None
    subid=models.AutoField(primary_key=True)
    subname=models.CharField(max_length=25)

