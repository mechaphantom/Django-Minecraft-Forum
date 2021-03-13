from django.contrib import admin
from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('register/',views.register, name ="register"),
    path('login/',views.loginUser, name ="login"),
    path('logout/',views.logoutUser, name ="logout"),
    path('edit/',views.edit_profile, name ="edit"),
    path('change/',views.changeprofile, name ="changeprofile"),
    path('updateprofile/',views.updateprofile, name ="updateprofile"),
    path('change-password/',views.change_password, name ="change_password"),
]
