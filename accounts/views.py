from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def UserRegisterView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        value = {'username': username, 'email': email}

        if password1 != password2:
            messages.error(request, "Passwords do not match. Please try again.")
            return render(request, "signup.html", {"value": value})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already registered, please choose another.")
            return render(request, "signup.html", {"value": value})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use, please use a different one.")
            return render(request, "signup.html", {"value": value})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect("login")

    return render(request, "signup.html")


def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials, please try again.")
            return render(request, "login.html")

    return render(request, "login.html")


def logout(request):
    auth_logout(request)
    return redirect("/")
