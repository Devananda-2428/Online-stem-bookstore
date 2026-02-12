from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name="index1"),
    path('login',views.login,name="login"),
    path('authorreg/',views.authorreg,name="authorreg"),
    path('userreg/',views.userreg,name="userreg"),
    path('forgotpass/',views.forgotpass,name="forgotpass")
]