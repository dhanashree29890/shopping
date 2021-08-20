from django.shortcuts import render


# Create your views here.
from django.db import models
from django.shortcuts import redirect, render
import socket
from django.http import HttpResponse, response
from products.models import Products
from cart.models import CartItem, Cart
import string
import random  # define the random module
import hashlib
import requests
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Sum

# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    try:
        socket.inet_aton(ip)
        ip_valid = True
        print("ip add is", ip)
    except socket.error:
        print("invalid ip")
        ip_valid = False
    items = 0
    if Cart.objects.filter(userip=ip).exists():
        cart = Cart.objects.get(userip=ip)
        print(cart)
        if CartItem.objects.filter(cart=cart.id).exists():
            tot = CartItem.objects.filter(cart=cart.id).aggregate(tot=Sum("quantity"))
            items = tot["tot"]
    return ip, items


def home(request):
    ip, items = get_client_ip(request)

    request.session["userip"] = ip
    request.session["items"] = items
    response = render(request, "index.html")  # django.http.HttpResponse

    return response
    # return render(request,"index.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


@csrf_protect
@csrf_exempt
def success(request):
    print(request)
    return render(request, "success.html")


@csrf_protect
@csrf_exempt
def failure(request):
    print(request)
    return render(request, "failure.html")


def view_products(request):
    products = Products.objects.all()

    response = render(request, "products.html", {"products": products})

    return response


def addtocart(request, id):
    prod = Products.objects.get(id=id)
    prod.quantity = prod.quantity - 1
    prod.save()
    if Cart.objects.filter(userip=request.session["userip"]).exists():
        pass
    else:
        Cart.objects.create(userip=request.session["userip"])
    cart = Cart.objects.get(userip=request.session["userip"])
    if CartItem.objects.filter(product=prod).exists():
        item = CartItem.objects.get(product=prod)
        item.quantity = item.quantity + 1
        item.save()
    else:
        CartItem.objects.create(
            product=prod, price_ht=prod.cost, cart=cart
        )  # ,quantity=1 )
    tot = CartItem.objects.filter(cart=cart.id).aggregate(tot=Sum("quantity"))
    request.session["items"] = tot["tot"]
    products = Products.objects.all()
    return render(request, "products.html", {"products": products})


def buy(request, id):
    prod = Products.objects.get(id=id)
    prod.quantity = prod.quantity - 1
    prod.save()
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        productinfo = prod.name
        amount = prod.cost

        S = 6  # number of characters in the string.
        # call random.choices() string module to find the string in Uppercase + numeric data.
        txnid = "".join(random.choices(string.ascii_uppercase + string.digits, k=S))
        print(
            "The randomly generated string is : " + str(txnid)
        )  # print the random data

        surl = "http://49.206.42.79:8000/success"
        furl = "http://49.206.42.79:8000/failure"
        url = "https://test.payu.in/_payment"
        key = "3I5M6C"  # "gtKFFx"
        SALT = "bqXwlIi7"  # "eCwWELxi"
        hashstring = (
            key
            + "|"
            + txnid
            + "|"
            + str(amount)
            + "|"
            + productinfo
            + "|"
            + firstname
            + "|"
            + email
            + "|||||||||||"
            + SALT
        )
        hash = hashlib.sha512(hashstring.encode("utf-8")).hexdigest().lower()
        data = {
            "key": key,
            "txnid": txnid,
            "amount": float(amount),
            "productinfo": productinfo,
            "firstname": firstname,
            "email": email,
            "phone": phone,
            "lastname": lastname,
            "hash": hash,
            "surl": surl,
            "furl": furl,
        }
        response = requests.post(url, data)
        return redirect(response.url)

    return render(request, "buynow.html")
