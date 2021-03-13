from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, LoginForm, UserChangeForm, EditProfileForm, PasswordChangeForm, ProfileChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from article.models import Profile
# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None)
    
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()
        login(request, newUser)
        messages.success(request, "Başarıyla Kayıt Oldunuz!")

        return redirect("index")
   
    context = {
            "form" : form
        }
    return render(request, "register.html", context)  

"""   
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            newUser = User(username = username)
            newUser.set_password(password)
            newUser.save()
            login(request, newUser)

            return redirect("index")
        context = {
            "form" : form
        }
        return render(request, "register.html", context) 
    
    else:
        form = RegisterForm()
        context = {
            "form" : form
        }
        return render(request, "register.html", context)
"""

def loginUser(request):
    form = LoginForm(request.POST or None)

    context = {
        "form" : form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password = password)

        if user is None:
            messages.warning(request, "Kullanıcı Adı veya Parola Hatalı!")
            return render(request,"login.html", context)
        
        messages.success(request, "Başarıyla Giriş Yaptınız!")
        login(request,user)
        return redirect("index")
    return render(request, "login.html", context)

def logoutUser(request):
    logout(request)
    messages.warning(request, "Çıkış Yapıldı.")
    return redirect("index")

def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profiliniz Başarıyla Güncellendi!")
            return redirect("/articles/dashboard")
    
    else:
        form = EditProfileForm(instance = request.user)
        args = {'form':form}
        return render(request, "edit.html", args)

def changeprofile(request):
    form = ProfileChangeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        change = form.save(commit=False)
        change.user = request.user
        change.save()
        messages.success(request, "Profiliniz Başarıyla Güncellendi!")
        return redirect("/articles/dashboard")

    return render(request, "change.html", {"form":form})

def updateprofile(request):
    form = ProfileChangeForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        change = form.save(commit=False)
        change.user = request.user
        change.save()
        messages.success(request, "Profiliniz Başarıyla Güncellendi!")
        return redirect("/articles/dashboard")

    return render(request, "updateprofile.html", {"form":form})    

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Profiliniz Başarıyla Güncellendi!")
            return redirect("/articles/dashboard")
        else:
            return redirect("/user/change-password")
    else:
        form = PasswordChangeForm(user = request.user)
        
        args = {'form':form}
        return render(request, "change_password.html", args)
