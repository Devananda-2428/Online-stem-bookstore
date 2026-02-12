from django.shortcuts import render, redirect
from . models import Login,Author,User
from Adminapp . models import Location
from django.http import HttpResponse
def index(request):
    return render(request,"Guest/index.html")

def login(request):
    if request.method=='POST':
        Username=request.POST.get("Username")
        Password=request.POST.get("Password")
        if Login.objects.filter(Username=Username,Password=Password).exists():
            Logindata=Login.objects.get(Username=Username,Password=Password)
            request.session['Uname']=Logindata.Username
            request.session['Loginid']=Logindata.Loginid
            role=Logindata.Role
            status=Logindata.Status
            if role=="admin":
                return redirect("/admin/adminhome")
            elif role=="Author":
                if Logindata.Status=="Confirmed":
                    return redirect("/author/authorhome")
                else:
                    return HttpResponse(
                        "<script>alert('Your confirmation is currently being processed.Please wait for the confirmation to be completed.');window.location='/';</script>")
            elif role=="User":
                return redirect("/user/index")
        else:

            return HttpResponse(
                "<script>alert('Incorrect UserName or Password');window.location='/login';</script>")

    else:
        return render(request,"Guest/login.html")

def authorreg(request):
    if request.method=='POST':
        at_name=request.POST.get('a_name')
        at_cont=request.POST.get('a_ph')
        at_em=request.POST.get('a_mail')
        at_adrs=request.POST.get('a_add')

        at_username=request.POST.get('a_usr')
        at_password=request.POST.get('a_pass')

        if Login.objects.filter(Username=at_username).exists():
            return HttpResponse(
                "<script>alert('Author with this username already exists');window.location='/';</script>")

        author1=Login()
        author1.Username=at_username
        author1.Password=at_password
        author1.Role="Author"
        author1.Status="Not Confirmed"
        author1.save()

        authorobj=Author()
        authorobj.Authorname=at_name
        authorobj.Authorcontact=at_cont
        authorobj.Authoremail=at_em
        authorobj.Authoraddress=at_adrs

        authorobj.Loginid=author1
        if len(request.FILES) != 0:
            at_img=request.FILES['authorimage']
        else:
            at_img='Images/default.jpg'
        authorobj.Authorimg=at_img
        authorobj.save()
        return HttpResponse(
                "<script>alert('Registration Successfull');window.location='/';</script>")
    else:
        return render(request,"Guest/authorreg.html")


def userreg(request):
    if request.method=='POST':
        us_name = request.POST.get('u_name')
        us_cont = request.POST.get('u_ph')
        us_em = request.POST.get('u_mail')
        us_loc = request.POST.get('u_loc')

        us_username = request.POST.get('u_usr')
        us_password = request.POST.get('u_pass')

        if Login.objects.filter(Username=us_username).exists():
            return HttpResponse(
                "<script>alert('User with this username already exists');window.location='/';</script>")

        user1=Login()
        user1.Username=us_username
        user1.Password=us_password
        user1.Role="User"
        user1.Status="Confirmed"
        user1.save()



        userobj=User()
        userobj.UserName = us_name
        userobj.Usercontact = us_cont
        userobj.Useremail = us_em

        userobj.Loginid = user1
        userobj.Locationid=Location.objects.get(Locationid= us_loc)

        userobj.save()
        return HttpResponse(
            "<script>alert('Registration Successfull');window.location='/';</script>")
    else:
        location=Location.objects.all()
        return render(request, "Guest/userreg.html",{'loc':location})


def forgotpass(request):
    if request.method=='POST':
        em=request.POST.get('usermail')
        p=request.POST.get('newpass')
        if Author.objects.filter(Authoremail=em).exists():
            author = Author.objects.get(Authoremail=em)
            login_instance = author.Loginid
            login_instance.Password = p
            login_instance.save()
            return HttpResponse(
                "<script>alert('Password Changed Successfully');window.location='/login';</script>")


        elif User.objects.filter(Useremail=em).exists():
            user = User.objects.get(Useremail=em)
            login_instance = user.Loginid
            login_instance.Password = p
            login_instance.save()
            return HttpResponse(
                "<script>alert('Password Changed Successfully');window.location='/login';</script>")
        else:
            return HttpResponse(
                "<script>alert('Not a Registered Author/User.');window.location='/';</script>")
    else:
        return render(request,"Guest/forgotpass.html")

