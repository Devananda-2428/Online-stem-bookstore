from django.shortcuts import render
from . models import District,Location,Tbl_Category,Subcategory
from Guestapp . models import Author,Login,User
from Authorapp . models import Book
from Userapp . models import Secondhandbook,Booking,Bookingmaster
from django.http import HttpResponse,JsonResponse

def adminhome(request):
    return render(request,'Admin/index.html')

def formview(request):
    return render(request,'Admin/form.html')



def district(request):
    if request.method=='POST':
        District_name=request.POST.get("distname")
        dt=District()

        if District.objects.filter(DistrictName=District_name).exists():
            return HttpResponse(
                "<script>alert('District Name Already exists');window.location='/admin/districtview';</script>")
        dt.DistrictName=District_name
        dt.save()
        return HttpResponse("<script>alert('District Inserted');window.location='/admin/districtview';</script>")
    else:
        return render(request,"Admin/districtreg.html")


def locationreg(request):
    if request.method=='POST':
        Districtid=request.POST.get("Districtid")

        Locationname=request.POST.get("locname")
        #return HttpResponse(Location)
        locobj=Location()
        if Location.objects.filter(DistrictId=Districtid,LocationName=Locationname).exists():
            return HttpResponse("<script>alert('Location Name Already Exist');window.location='/Admin/locationreg';</script>")
        locobj.DistrictId=District.objects.get(DistrictId=Districtid)

        locobj.LocationName=Locationname
        locobj.save()

        return HttpResponse("<script>alert('Location Inserted');window.location='/admin/locationview';</script>")

    else:
        dist=District.objects.all()
        return render(request,"Admin/locationreg.html",{'district':dist})

def Categoryreg(request):
    if request.method == 'POST':
        catname = request.POST.get("Category")
        catobj = Tbl_Category()
        catobj.Categoryname = catname
        if len(request.FILES) != 0:
            catimg = request.FILES['Categoryimage']
        else:
            catimg = 'Images/default.jpg'
        catobj.Categoryimg = catimg
        catobj.save()
        return HttpResponse(
            "<script>alert('Category Registered Sucessfully');window.location='/admin/categoryview';</script>")
    else:
        return render(request, "Admin/Categoryreg.html")

def districtview(request):
    dst=District.objects.all()
    return render(request,"Admin/districtview.html",{'dstrt':dst})

def districtdelete(request,id):
    dt=District.objects.get(DistrictId=id)
    dt.delete()
    return HttpResponse("<script>alert('District Deleted');window.location='/admin/districtview';</script>")

def districtedit(request, id):
    if request.method == 'POST':
        scat = District.objects.get(DistrictId=id)
        scat.DistrictName = request.POST.get('dit')

        scat.save()
        return districtview(request)
    else:
        subcategory = District.objects.get(DistrictId=id)
        return render(request, "Admin/districtedit.html", {'Scat': subcategory})

def locationview(request):
    loc = Location.objects.all()
    dist = District.objects.all()
    return render(request, "Admin/locationview.html", {'location': loc, 'district': dist})


def locationbyid(request):
    did=int(request.POST.get("did"))
    location=Location.objects.filter(DistrictId=did).values()
    return JsonResponse(list(location),safe=False)


def locationedit(request, id):
    if request.method == 'POST':
        Districtid = request.POST.get("Districtid")
        Loction = request.POST.get("Location")
        loc = Location.objects.get(Locationid=id)
        loc.LocationName = Loction
        loc.DistrictId = District.objects.get(DistrictId=Districtid)
        loc.save()
        return locationview(request)
    else:
        loct = Location.objects.get(Locationid=id)
        dist = District.objects.all()
        return render(request, "Admin/locationedit.html", {'loc': loct, 'dist': dist})

def locationdelete(request, id):
    loc = Location.objects.get(Locationid=id)
    loc.delete()
    return HttpResponse("<script>alert('Location Deleted');window.location='/admin/locationview';</script>")


def categoryview(request):
    cate = Tbl_Category.objects.all()
    return render(request, "Admin/categoryview.html", {'category': cate})

def categoryedit(request, id):
    if request.method == 'POST':
        cate = Tbl_Category.objects.get(Categoryid=id)
        cate.Categoryname = request.POST.get('Category')
        if len(request.FILES) == 0:
            cate.Categoryimg = request.POST.get("Categoryimage")
        else:
            cate.Categoryimg = request.FILES["Categoryimage"]
        cate.save()
        return HttpResponse("<script>alert('Category Updated');window.location='/admin/categoryview';</script>")
    else:
        category = Tbl_Category.objects.get(Categoryid=id)
        return render(request, "Admin/categoryedit.html", {'cat': category})

def categorydelete(request, id):
    cate = Tbl_Category.objects.get(Categoryid=id)
    cate.delete()
    return categoryview(request)

def confirm(request, id):
    lob=Login.objects.get(Loginid=id)
    lob.Status="Confirmed"
    lob.save()
    return HttpResponse("<script>alert('Author Confirmation Successfull');window.location='/admin/authorconfirm';</script>")


def authorconfirm(request):
    authors = Author.objects.filter(Loginid__Status="Not Confirmed")
    return render(request,"Admin/authorconfirm.html",{'auth':authors})

def bookconfirm(request):
    bok=Book.objects.filter(status="Not Confirmed")
    return render(request,"Admin/bookconfirm.html",{'books':bok})


def bookconfirmation(request,id):
    bk=Book.objects.get(Bookid=id)
    bk.status="Confirmed"
    bk.save()
    return HttpResponse(
        "<script>alert('Book Confirmation Successfull');window.location='/admin/bookconfirm';</script>")

def subcategoryreg(request):
    if request.method=='POST':
        sub_name=request.POST.get("subcatname")
        sub=Subcategory()

        if Subcategory.objects.filter(subname=sub_name).exists():
            return HttpResponse(
                "<script>alert('Sub-category  Already exists');windows.location='/Admin/subcatview';</script>")
        sub.subname=sub_name
        sub.save()
        return HttpResponse("<script>alert('Sub-category Added');window.location='/admin/subcatview';</script>")
    else:
        return render(request,"Admin/subcategoryreg.html")


def subcatview(request):
    subc=Subcategory.objects.all()
    return render(request, "Admin/subcatview.html", {'subcategory': subc})

def subcatedit(request, id):
    if request.method == 'POST':
        scat = Subcategory.objects.get(subid=id)
        scat.subname = request.POST.get('subcat')

        scat.save()
        return subcatview(request)
    else:
        subcategory = Subcategory.objects.get(subid=id)
        return render(request, "Admin/subcatedit.html", {'Scat': subcategory})

def subcatdelete(request,id):
    cat = Subcategory.objects.get(subid=id)
    cat.delete()
    return subcatview(request)

def secbookconfirm(request):
    sc=Secondhandbook.objects.filter(status="Not Confirmed")
    return render(request,"Admin/secbookconfirm.html",{'scbooks':sc})

def secbookconfirmation(request,id):
    scbk = Secondhandbook.objects.get(Secbookid=id)
    scbk.confirmation="Confirmed"
    scbk.status="For Sale"
    scbk.save()
    return HttpResponse(
        "<script>alert('Book Confirmation Successfull');window.location='/admin/secbookconfirm';</script>")

def authordetails(request):
    authors = Author.objects.filter(Loginid__Status="Confirmed")
    return render(request, "Admin/authordetails.html", {'auth':authors})

def authorbooks(request,id):
    books=Book.objects.filter(Authorid=id,status="Confirmed")
    return render(request,"Admin/authorbooks.html",{'books':books})

def userdetails(request):
    users=User.objects.all()
    return render(request,"Admin/userdetails.html",{'users':users})

def bookdetails(request,id):
    Books=Book.objects.get(Bookid=id)
    return render(request,"Admin/bookdetails.html",{'Books':Books})

def salesview(request):
    s=Booking.objects.all()
    return render(request,"Admin/salesview.html",{'sales':s})

def adminchangepass(request):
    if request.method=='POST':
        passw= request.POST.get('new_pass')

        lid=request.session.get('Loginid')
        L=Login.objects.get(Loginid=lid)
        L.Password=passw
        L.save()
        return HttpResponse(
            "<script>alert('Password Changed Successfully');window.location='/admin/adminhome';</script>")

    else:
        return render(request,"Admin/adminchangepass.html")

def adminlogout(request):
    return render(request,"Guest/index.html")

def authordel(request,id):
    au=Author.objects.get(Authorid=id)
    au.delete()
    return authordetails(request)
