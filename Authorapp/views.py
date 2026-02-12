from django.shortcuts import render
from django.http import HttpResponse
from Adminapp.models import Language,Tbl_Category,Subcategory
from Guestapp.models import Author,Login
from . models import Book
from Userapp.models import Booking,Bookingmaster,Payment
# Create your views here.

def authorhome(request):
    id = request.session.get('Loginid')

    aid=Author.objects.get(Loginid=id)


    
    return render(request,"Author/index.html",{'author':aid})

def bookreg(request):
    if request.method=='POST':
        bk_name=request.POST.get('b_name')
        bk_isbn = request.POST.get('b_num')
        bk_year=request.POST.get('b_year')
        bk_catgry = request.POST.get('b_cat')
        bk_language = request.POST.get('b_lang')
        bk_price = request.POST.get('b_price')
        bk_stock=request.POST.get('b_stock')
        bk_sub=request.POST.get('b_subcat')

        if Book.objects.filter(Bookisbn=bk_isbn).exists():
            return HttpResponse(
                "<script>alert('Book with this ISBN already exists');window.location='/author/authorhome';</script>")

        books=Book()
        books.Authorid=Author.objects.get(Loginid=request.session['Loginid'])
        books.Categoryid=Tbl_Category.objects.get(Categoryid=bk_catgry)
        books.Langid=Language.objects.get(Langid=bk_language)
        books.subid=Subcategory.objects.get(subid=bk_sub)


        books.Bookname=bk_name
        books.Bookyear=bk_year
        books.Bookisbn=bk_isbn
        books.Bookprice=bk_price
        books.Bookstock=bk_stock
        books.status="Not Confirmed"
        if len(request.FILES)!=0:
            bk_img = request.FILES['bookimage']
        else:
            bk_img='Images/default.jpg'
        books.Bookcover=bk_img

        if len(request.FILES)!=0:
            bk_pdf=request.FILES['bookfile']
        else:
            bk_pdf='Images/default.jpg'
        books.Bookpdf=bk_pdf
        books.save()
        return HttpResponse(
            "<script>alert('Registration Successfull');window.location='/author/authorhome';</script>")
    else:
        lang = Language.objects.all()
        cat = Tbl_Category.objects.all()
        scat=Subcategory.objects.all()
        return render(request, "Author/bookreg.html", {'lanuages': lang, 'categories': cat,'subcategory':scat})

def sales(request):
    aid=request.session.get('Loginid')
    author=Author.objects.get(Loginid=aid)
    id=author.Authorid
    details=Booking.objects.filter(Authorid=id,Masterid__status="Hardcopy")
    return render(request,"Author/sales.html",{'details':details})

def pdfsales(request):
    aid=request.session.get('Loginid')
    author=Author.objects.get(Loginid=aid)
    id=author.Authorid
    details=Booking.objects.filter(Authorid=id,Masterid__status="pdf")
    return render(request,"Author/pdfsales.html",{'details':details})

def ebooksales(request):
    aid=request.session.get('Loginid')
    author=Author.objects.get(Loginid=aid)
    id=author.Authorid
    details=Booking.objects.filter(Authorid=id,Masterid__status="ebook")
    return render(request,"Author/ebooksales.html",{'details':details})


def authorinvoice(request,id):
    d=Booking.objects.filter(Bookingid=id)
    p=Payment.objects.filter(Bookingid=id)
    return render(request,"Author/authorinvoice.html",{'d':d,'p':p})

def viewbooks(request):
    id = request.session.get('Loginid')
    author = Author.objects.get(Loginid=id)
    aid=author.Authorid
    data=Book.objects.filter(Authorid=aid)
    return render(request,"Author/viewbooks.html",{'data':data})

def bookupdate(request,id):
    d1=Book.objects.get(Bookid=id)
    return render(request,"Author/bookupdate.html",{'d1':d1})

def update(request,id):
    if request.method=='POST':
        price=request.POST.get('new_price')
        stock=request.POST.get('new_stock')

        b1=Book.objects.get(Bookid=id)
        b1.Bookprice=price
        b1.Bookstock=stock
        b1.save()
    return HttpResponse(
        "<script>alert('Updated Successfully');window.location='/Author/viewbooks';</script>")

def delete(request,id):
    b=Book.objects.get(Bookid=id)
    b.delete()
    return HttpResponse(
        "<script>alert('Book Deleted');window.location='/author/delete';</script>")


def editprofile(request,id):
    if request.method=='POST':
        name = request.POST.get('newname')
        cont = request.POST.get('newcont')
        mail = request.POST.get('newmail')
        add = request.POST.get('newadd')
        uname = request.POST.get('newuser')
        pwrd = request.POST.get('newpass')

        lid=request.session.get('Loginid')
        Auth=Login.objects.get(Loginid=lid)
        Auth.Username=uname
        Auth.Password=pwrd
        Auth.save()


        A=Author.objects.get(Authorid=id)
        A.Authorname=name
        A.Authorcontact=cont
        A.Authoremail=mail
        A.Authoraddress=add
        A.save()
        return HttpResponse(
            "<script>alert('Profile Updated');window.location='/author/authorhome';</script>")
    else:
        data=Author.objects.get(Authorid=id)
        return render(request,"Author/editprofile.html",{'data':data})