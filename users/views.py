from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import requests
from django.contrib.auth import get_user_model, login, logout, authenticate

User = get_user_model()
# Create your views here.


def user_logout(request):
    logout(request)

    try:
        del request.session["jwt"]

    except:
        pass
    return redirect("/")


def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        # is_admin = request.POST["is_admin"]
        user = authenticate(email=email, password=password)
        print("trying login")

        if user is not None:
            login(request, user)
            resp = requests.post(
                "http://127.0.0.1:8000/api/token/",
                data={"email": email, "password": password},
            )
            jwt_token = resp.json()["access"]
            request.session["jwt"] = jwt_token
            seller = User.objects.get(email=email, is_admin=True)
            print(request.session["jwt"])
            if seller:
                return redirect("/products/manage_products/" + str(seller.id))

            else:
                return redirect("/", {user: user})
        else:
            messages.info(request, "invalid credentials")
            return redirect("login")
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":

        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        is_admin = request.POST["is_admin"]
        if password1 != password2:
            messages.info(request, "password mismatch")
            return redirect("register")
        elif User.objects.filter(email=email).exists():
            print("email exists")
            messages.info(request, "email exists")
            return redirect("register")

        else:
            user = User.objects.create_user(
                password=password1, email=email, is_admin=is_admin
            )
            user.save()

            messages.info(request, "user created")
            return redirect("login")

    else:
        return render(request, "register.html")
