from django.db import models
from Guestapp.models import Author
from Adminapp.models import Tbl_Category,Language,Subcategory

class Book(models.Model):
    objects=None
    Bookid=models.AutoField(primary_key=True)
    Authorid=models.ForeignKey(Author,on_delete=models.CASCADE)
    Bookname=models.CharField(max_length=50)
    Bookyear=models.DateField()
    Bookisbn=models.BigIntegerField()
    Bookprice=models.BigIntegerField()
    Categoryid=models.ForeignKey(Tbl_Category,on_delete=models.CASCADE)
    Langid=models.ForeignKey(Language,on_delete=models.CASCADE)
    Bookcover=models.ImageField()
    Bookregdate=models.DateField(auto_now_add=True)
    Bookstock=models.BigIntegerField()
    Bookpdf=models.FileField()
    status=models.CharField(max_length=25)
    subid=models.ForeignKey(Subcategory,on_delete=models.CASCADE,default=None)




