from django.urls import path
from . import views
urlpatterns = [
    path('authorhome/',views.authorhome,name="authorhome"),
    path('bookreg/',views.bookreg,name="bookreg"),
    path('sales/',views.sales,name="sales"),
    path('authorinvoice/<int:id>',views.authorinvoice,name="authorinvoice"),
    path('viewbooks/',views.viewbooks,name="viewbooks"),
    path('bookupdate/<int:id>',views.bookupdate,name="bookupdate"),
    path('update/<int:id>',views.update,name="update"),
    path('delete/<int:id>',views.delete,name="delete"),
    path('pdfsales/',views.pdfsales,name="pdfsales"),
    path('ebooksales/',views.ebooksales,name="ebooksales"),
    path('editprofile/<int:id>',views.editprofile,name="editprofile")
]