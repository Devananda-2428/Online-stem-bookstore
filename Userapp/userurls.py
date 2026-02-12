from django.urls import path
from . import views

urlpatterns=[
    path('index/',views.index,name="index"),

    path('science/<int:id>',views.science,name="science"),
    path('sbookdetails/<int:id>',views.sbookdetails,name="sbookdetails"),
    path('textbook/<int:id>',views.textbook,name="textbook"),
    path('guides/<int:id>',views.guides,name="guides"),
    path('questionbank/<int:id>',views.questionbank,name="questionbank"),
    path('secondhand/<int:id>',views.secondhand,name="secondhand"),

    path('secondbookdetails/<int:id>',views.secondbookdetails,name="secondbookdetails"),
    path('secbookpurchase/<int:id>',views.secbookpurchase,name="secbookpurchase"),
    path('secbookconfirm/<int:id>',views.secbookconfirm,name="secbookconfirm"),

    path('buynow/<int:id>',views.buynow,name="buynow"),
    path('paynow/<int:id>',views.paynow,name="paynow"),
    path('paymentpage/<int:id>',views.paymentpage,name="paymentpage"),
    path('payment/<int:id>',views.payment,name="payment"),

    path('hcopy/<int:id>',views.hcopy,name="hcopy"),
    path('payment1/<int:id>',views.payment1,name="payment1"),
    path('paymentpage1/<int:id>',views.paymentpage1,name="paymentpage1"),

    path('ebook/<int:id>', views.ebook, name="ebook"),
    path('payment2/<int:id>',views.payment2,name="payment2"),
    path('paymentpage2/<int:id>',views.paymentpage2,name="paymentpage2"),

    path('confirm/',views.confirm,name="confirm"),
    path('confirm1/',views.confirm1,name="confirm1"),
    path('confirm2/',views.confirm2,name="confirm2"),
    path('confirm3/',views.confirm3,name="confirm3"),

    path('orders/',views.orders,name="orders"),
    path('invoice/<int:id>',views.invoice,name="invoice"),

    path('secbookreg/',views.secbookreg,name="secbookreg"),
    path('secbookview/',views.secbookview,name="secbookview"),
    path('secrequest/<int:id>',views.secrequest,name="secrequest"),
    path('secconfirm/<int:id>',views.secconfirm,name="secconfirm"),
    path('delrequest/<int:id>',views.delrequest,name="delrequest"),
    path('delsecbook/<int:id>',views.delsecbook,name="delsecbook"),

    path('search/',views.search,name="search"),
    path('searchbook/',views.searchbook,name="searchbook"),

    path('userlogout/',views.userlogout,name="userlogout")





]