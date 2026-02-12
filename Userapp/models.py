from django.db import models
from Authorapp.models import Book
from Guestapp. models import User,Author
from Adminapp.models import Tbl_Category,Language,Subcategory
from django.core.validators import MaxLengthValidator
# Create your models here.
class Bookingmaster(models.Model):
    Masterid=models.AutoField(primary_key=True)
    Billnum=models.BigIntegerField()
    Date=models.DateField(auto_now_add=True)
    Amount=models.BigIntegerField()
    status=models.CharField(max_length=50)


class Booking(models.Model):
    Bookingid=models.AutoField(primary_key=True)
    Bookid=models.ForeignKey(Book,on_delete=models.CASCADE)
    Userid=models.ForeignKey(User,on_delete=models.CASCADE)
    Useraddress=models.CharField(max_length=50,blank=True,null=True)
    Copynum=models.BigIntegerField()
    Total=models.BigIntegerField()
    Masterid=models.ForeignKey(Bookingmaster,on_delete=models.CASCADE)
    Authorid=models.ForeignKey(Author,on_delete=models.CASCADE)

class Payment(models.Model):
    Paymentid=models.AutoField(primary_key=True)
    Payment_date=models.DateField(auto_now_add=True)
    Cardname=models.CharField(max_length=25)
    Cardnumber=models.BigIntegerField(validators=[MaxLengthValidator(limit_value=16, message="Card number must be 16 digits")])
    Cardtype=models.CharField(max_length=15)
    Expiry=models.DateField()
    cvv=models.IntegerField()
    status=models.CharField(max_length=15)
    Bookingid=models.ForeignKey(Booking,on_delete=models.CASCADE)


class Secondhandbook(models.Model):
    Secbookid=models.AutoField(primary_key=True)
    secbookname=models.CharField(max_length=50)
    Sec_author=models.CharField(max_length=50)
    Categoryid=models.ForeignKey(Tbl_Category,on_delete=models.CASCADE)
    Langid=models.ForeignKey(Language,on_delete=models.CASCADE)
    subid=models.ForeignKey(Subcategory,on_delete=models.CASCADE,default=None)
    secbookimg=models.ImageField()
    secbookprice=models.BigIntegerField()
    secbookregdate=models.DateField(auto_now_add=True)
    confirmation=models.CharField(max_length=25)
    status=models.CharField(max_length=25)
    stock=models.IntegerField()
    Userid=models.ForeignKey(User,on_delete=models.CASCADE)

class Secbookrequest(models.Model):
    Requestid = models.AutoField(primary_key=True)
    Secbookid = models.ForeignKey(Secondhandbook,on_delete=models.CASCADE)
    Requestdate = models.DateField(auto_now_add=True)
    Userid = models.ForeignKey(User,on_delete=models.CASCADE)
    Paymentstatus = models.CharField(max_length=15)

