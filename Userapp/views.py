from django.db.models import Max, Count
from django.shortcuts import render
from django.http import HttpResponse
from .models import Bookingmaster, Booking, Payment, Secondhandbook, Secbookrequest
from Adminapp.models import Language, Tbl_Category, Subcategory
from Authorapp.models import Book
from Guestapp.models import User, Author
from datetime import date
from django.http import JsonResponse


def index(request):
    cat = Tbl_Category.objects.all()
    return render(request, "User/index.html", {'category': cat})


def textbook(request,id):
    bks = Book.objects.filter(status="Confirmed", Categoryid=id, subid__subname="TextBook")
    cat = Tbl_Category.objects.get(Categoryid=id)
    return render(request, "User/textbook.html", {'category': cat, 'books': bks})


def guides(request, id):
    bks = Book.objects.filter(status="Confirmed", Categoryid=id, subid__subname="Guide")
    cat = Tbl_Category.objects.get(Categoryid=id)
    return render(request, "User/guide.html", {'category': cat, 'books': bks})

def questionbank(request, id):
    bks = Book.objects.filter(status="Confirmed", Categoryid=id, subid__subname="Question Bank")
    cat = Tbl_Category.objects.get(Categoryid=id)
    return render(request, "User/questionbank.html", {'category': cat, 'books': bks})




def science(request,id):
    book = Book.objects.filter(status="Confirmed", Categoryid=id)[:6]
    cats = Tbl_Category.objects.get(Categoryid=id)
    return render(request, "User/science.html", {'books': book, 'category': cats})


def sbookdetails(request, id):
    sbook = Book.objects.get(Bookid=id)
    return render(request, "User/sbookdetails.html", {'Sbooks': sbook})


def buynow(request, id):
    bk = Book.objects.get(Bookid=id)
    return render(request, "User/buynow.html", {'books': bk})


def paynow(request, id):
    bks = Book.objects.get(Bookid=id)
    bprice = bks.Bookprice
    pdf_price = bprice - 100
    request.session['Pdf_price'] = pdf_price
    current_date = date.today()
    return render(request, "User/pdfpurchase.html", {'books': bks, 'pdfprice': pdf_price, 'current_date': current_date})


def payment(request, id):
    return render(request, "User/payment.html", {'books': id})


def paymentpage(request, id):
    if request.method == 'POST':
        cardname = request.POST.get('card_name')
        cardnum = request.POST.get('card_number')
        cardtype = request.POST.get('card_type')
        expdate = request.POST.get('exp_date')
        usercvv = request.POST.get('cvv')

        master = Bookingmaster()
        max_value = Bookingmaster.objects.aggregate(max_value=Max('Billnum'))['max_value']

        if max_value is None:
            max_value = 1
        else:
            max_value += 1

        master.Billnum = max_value
        pdf_price = request.session.get('Pdf_price')
        master.Amount = pdf_price
        master.status = "pdf"
        master.save()

        details = Booking()
        bk = Book.objects.get(Bookid=id)
        details.Bookid = bk
        details.Userid = User.objects.get(Loginid=request.session['Loginid'])
        details.Copynum = 1
        details.Total = request.session.get('Pdf_price')

        authid = bk.Authorid
        details.Authorid = authid
        details.Masterid = master
        details.save()

        pay = Payment()
        pay.Cardname = cardname
        pay.Cardnumber = cardnum
        pay.Cardtype = cardtype
        pay.Expiry = expdate
        pay.cvv = usercvv
        pay.status = "Paid"
        pay.Bookingid = details
        pay.save()
    return render(request, "User/confirm.html")


def hcopy(request, id):
    if request.method == 'POST':
        add = request.POST.get('address')
        request.session['Address'] = add
        return render(request, "User/payment1.html", {'books': id})

    else:
        bk = Book.objects.get(Bookid=id)
        current_date = date.today()
        return render(request, "User/hcpurchase.html", {'books': bk, 'current_date': current_date})


def payment1(request, id):
    return render(request, "User/payment1.html", {'books': id})


def paymentpage1(request, id):
    if request.method == 'POST':
        cardname = request.POST.get('card_name')
        cardnum = request.POST.get('card_number')
        cardtype = request.POST.get('card_type')
        expdate = request.POST.get('exp_date')
        usercvv = request.POST.get('cvv')

        bk = Book.objects.get(Bookid=id)

        master = Bookingmaster()
        max_value = Bookingmaster.objects.aggregate(max_value=Max('Billnum'))['max_value']
        # return HttpResponse(max_value)
        if max_value is None:
            max_value = 1
        else:
            max_value += 1

        master.Billnum = max_value
        b_price = bk.Bookprice
        master.Amount = b_price
        master.status = "Hardcopy"
        master.save()

        details = Booking()

        details.Bookid = bk
        details.Userid = User.objects.get(Loginid=request.session['Loginid'])
        details.Copynum = 1
        details.Total = bk.Bookprice

        authid = bk.Authorid
        details.Authorid = authid
        details.Masterid = master
        details.Useraddress = request.session.get('Address')
        details.save()

        pay = Payment()
        pay.Cardname = cardname
        pay.Cardnumber = cardnum
        pay.Cardtype = cardtype
        pay.Expiry = expdate
        pay.cvv = usercvv
        pay.status = "Paid"
        pay.Bookingid = details
        pay.save()

        stock = bk.Bookstock
        stock -= 1
        bk.Bookstock = stock
        bk.save()

    return render(request, "User/confirm1.html")


def ebook(request, id):
    if request.method == 'POST':
        eadd = request.POST.get('kid')
        request.session['ebook_address'] = eadd
        return render(request, "User/payment2.html", {'books': id})
    else:
        bk = Book.objects.get(Bookid=id)
        b_price = bk.Bookprice
        ebprice = b_price - 200
        request.session['Ebook_price'] = ebprice
        current_date = date.today()
        return render(request, "User/epurchase.html", {'books': bk, 'ebprice': ebprice, 'current_date': current_date})


def payment2(request, id):
    return render(request, "User/payment2.html", {'books': id})


def paymentpage2(request, id):
    if request.method == 'POST':
        cardname = request.POST.get('card_name')
        cardnum = request.POST.get('card_number')
        cardtype = request.POST.get('card_type')
        expdate = request.POST.get('exp_date')
        usercvv = request.POST.get('cvv')

        bk = Book.objects.get(Bookid=id)

        master = Bookingmaster()
        max_value = Bookingmaster.objects.aggregate(max_value=Max('Billnum'))['max_value']
        # return HttpResponse(max_value)
        if max_value is None:
            max_value = 1
        else:
            max_value += 1

        master.Billnum = max_value
        eb_price = request.session.get('Ebook_price')
        master.Amount = eb_price
        master.status = "ebook"
        master.save()

        details = Booking()

        details.Bookid = bk
        details.Userid = User.objects.get(Loginid=request.session['Loginid'])
        details.Copynum = 1
        details.Total = request.session.get('Ebook_price')

        authid = bk.Authorid
        details.Authorid = authid
        details.Masterid = master
        details.Useraddress = request.session.get('ebook_address')
        details.save()

        pay = Payment()
        pay.Cardname = cardname
        pay.Cardnumber = cardnum
        pay.Cardtype = cardtype
        pay.Expiry = expdate
        pay.cvv = usercvv
        pay.status = "Paid"
        pay.Bookingid = details
        pay.save()
    return render(request, "User/confirm2.html")


def confirm(request):
    if request.method == 'POST':
        cat = Tbl_Category.objects.all()
        return render(request, "User/index.html", {'category': cat})
    else:
        return render(request, "User/confirm.html")


def confirm1(request):
    if request.method == 'POST':
        cat = Tbl_Category.objects.all()
        return render(request, "User/index.html", {'category': cat})
    else:
        return render(request, "User/confirm1.html")


def confirm2(request):
    if request.method == 'POST':
        cat = Tbl_Category.objects.all()
        return render(request, "User/index.html", {'category': cat})
    else:
        return render(request, "User/confirm2.html")


def orders(request):
    uid = request.session.get('Loginid')
    user = User.objects.get(Loginid=uid)
    id = user.Userid
    details = Booking.objects.filter(Userid=id).order_by('-Bookingid')
    return render(request, "User/orders.html", {'details': details})


def invoice(request, id):
    d1 = Booking.objects.filter(Bookingid=id)
    d2 = Payment.objects.filter(Bookingid=id)
    return render(request, "User/invoice.html", {'d1': d1, 'd2': d2})


def secbookreg(request):
    if request.method == 'POST':
        sbk_name = request.POST.get('sb_name')
        sbk_aname = request.POST.get('sb_aname')
        sbk_cat = request.POST.get('sb_cat')
        sbk_type = request.POST.get('sb_subcat')
        sbk_lang = request.POST.get('sb_lang')
        or_price=request.POST.get('sbo_price')
        sbk_price = request.POST.get('sb_price')
        if or_price < sbk_price:
            return JsonResponse(
                {'message': 'THE SELLING PRICE SHOULD BE LESS THAN THE ORIGINAL BOOK PRICE.PLEASE NAVIGATE BACK TO RETURN TO THE REGISTRATION PAGE'},
                status=400)
        else:
            secbook = Secondhandbook()
            secbook.Categoryid = Tbl_Category.objects.get(Categoryid=sbk_cat)
            secbook.Langid = Language.objects.get(Langid=sbk_lang)
            secbook.subid = Subcategory.objects.get(subid=sbk_type)
            secbook.Userid = User.objects.get(Loginid=request.session['Loginid'])

            secbook.secbookname = sbk_name
            secbook.Sec_author = sbk_aname
            secbook.secbookprice = sbk_price
            secbook.confirmation = "Not Confirmed"
            secbook.status = "Not confirmed"
            secbook.stock = 1
            if len(request.FILES) != 0:
                sbk_img = request.FILES['secbookimage']
            else:
                sbk_img = 'Images/default.jpg'
            secbook.secbookimg = sbk_img
            secbook.save()
            return HttpResponse(
                "<script>alert('Registration Successfull');window.location='/user/index';</script>")
    else:
        l = Language.objects.all()
        c = Tbl_Category.objects.all()
        s = Subcategory.objects.all()
        return render(request, "User/secbookreg.html", {'lanuages': l, 'categories': c, 'subcategory': s})


def secondhand(request, id):
    scbk = Secondhandbook.objects.filter(confirmation="Confirmed", Categoryid=id, stock__gt=0)
    return render(request, "User/secondhandbook.html", {'sbooks': scbk})


def secondbookdetails(request, id):
    d1 = Secondhandbook.objects.get(Secbookid=id)
    return render(request, "User/secondbookdetails.html", {'data': d1})


def secbookpurchase(request, id):
    d1 = Secondhandbook.objects.get(Secbookid=id)
    current_date = date.today()
    return render(request, "User/secbookpurchase.html", {'data': d1, 'date': current_date})


def secbookconfirm(request, id):
    if request.method == 'POST':
        d = Secondhandbook.objects.get(Secbookid=id)

        secbook = Secbookrequest()
        secbook.Secbookid = d
        secbook.Userid = User.objects.get(Loginid=request.session['Loginid'])
        secbook.Paymentstatus = "Processing"
        secbook.save()

        d.status = "Booked"
        d.save()
    return render(request, "User/Confirm3.html")


def secbookview(request):
    id = request.session.get('Loginid')
    uid = User.objects.get(Loginid=id)
    user = uid.Userid
    data = Secondhandbook.objects.filter(Userid=user)
    return render(request, "User/secbookview.html", {'data': data})


def secrequest(request, id):
    dt = Secbookrequest.objects.get(Secbookid=id)
    return render(request, "User/secrequest.html", {'dt': dt})


def secconfirm(request, id):
    sec = Secondhandbook.objects.get(Secbookid=id)
    sec.stock = 0
    sec.status = "Sold"
    sec.save()
    d = Secbookrequest.objects.get(Secbookid=id)
    d.Paymentstatus = "Paid"
    d.save()
    return render(request, "User/confirm4.html")


def confirm3(request):
    if request.method == 'POST':
        cat = Tbl_Category.objects.all()
        return render(request, "User/index.html", {'category': cat})
    else:
        return render(request, "User/confirm3.html")


def delrequest(request, id):
    sb = Secondhandbook.objects.get(Secbookid=id)
    sb.status = "For Sale"
    sb.save()
    req = Secbookrequest.objects.get(Secbookid=id)
    req.delete()
    return secbookview(request)


def delsecbook(request, id):
    sec = Secondhandbook.objects.get(Secbookid=id)
    sec.delete()
    return secbookview(request)


def search(request):
    a = Tbl_Category.objects.all()
    b = Subcategory.objects.all()
    return render(request, "User/search.html", {'Category': a, 'Type': b})


def searchbook(request):
    if request.method == 'POST':
        bkname = request.POST.get('book')
        catgry = request.POST.get('cat')
        tp = request.POST.get('type')

        c1 = Tbl_Category.objects.get(Categoryid=catgry)
        cid = c1.Categoryid

        t1 = Subcategory.objects.get(subid=tp)
        tid = t1.subid
        details = Book.objects.filter(Bookname=bkname, Categoryid=cid, subid=tid)

        return render(request,"User/searchbookdetails.html",{'details':details})


def userlogout(request):
    return render(request,"Guest/index.html")