from django.shortcuts import render
from .models import Cart, CartItem
from django.http import JsonResponse
import json
import ast
from django.http import HttpResponse
from products.models import Products

# Create your views here.


def cart(request, ip):
    crt = Cart.objects.get(userip=ip)
    prods = CartItem.objects.filter(cart=crt)

    return render(request, "cart.html", {"products": prods})


def update_quant(request):

    prod_id = request.GET.get("prod_id")
    action = request.GET.get("action")
    change = request.GET.get("change")
    cartitem = request.GET.get("cartitem")
    prod = Products.objects.get(id=prod_id)
    if action == "add":
        prod.quantity = prod.quantity - 1
        request.sessions["items"] = request.session["items"] - 1
    else:
        prod.quantity = prod.quantity + 1
        request.sessions["items"] = request.session["items"] + 1
    prod.save()
    item = CartItem.objects.get(id=cartitem)
    item.quantity = change
    if item.quantity == 0:
        item.save()
    else:
        item.delete()
    return HttpResponse(prod_id)  # (context)
