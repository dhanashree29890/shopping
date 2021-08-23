from django.shortcuts import redirect, render
from .models import Products
import requests
from django import forms
from django.contrib import messages
from api.serializers import ProductUpdateSerializer


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ["name", "img", "cost", "quantity", "is_active"]


def delete_prod(request, id, seller_id):

    id = id
    address = "http://127.0.0.1:8000/api/delete/" + str(id)
    resp = requests.delete(
        address, headers={"Authorization": "Bearer " + request.session["jwt"]}
    ).text
    print(resp)
    return redirect("/products/manage_products/" + str(seller_id))


def update_prod(request, id):

    id = id
    address = "http://127.0.0.1:8000/api/getone/" + str(id)

    prod = requests.get(
        address, headers={"Authorization": "Bearer " + request.session["jwt"]}
    ).json()
    # product = Products.objects.get(id=id)
    seller = prod["seller"]

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES or None, instance=prod)
        if form.is_valid():
            print("trying to see form's img", form.cleaned_data["img"])
            resp = requests.post(
                "http://127.0.0.1:8000/api/update/" + str(id),
                files={"img": form.cleaned_data["img"]},  # request.FILES["img"]},
                headers={"Authorization": "Bearer " + request.session["jwt"]},
                data=form.data,
            )
            # print(resp)
            return redirect("/products/manage_products/" + str(seller))
        else:
            return redirect("/products/manage_products/" + str(seller))
    else:
        form = ProductForm(instance=prod)
        # instance={
        #     "name": prod["name"],
        #     "img": prod["img"],
        #     "cost": prod["cost"],
        #     "quantity": prod["quantity"],
        #     "is_active": prod["is_active"],
        # }

        # }prod)

    return render(request, "update_prod.html", {"prod": prod})  # , "form": form})


def manage_products(request, id):
    myform = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES or None)
        if form.is_valid():
            print(form.data)
            requests.post(
                url="http://127.0.0.1:8000/api/create",
                headers={"Authorization": "Bearer " + request.session["jwt"]},
                files={"img": request.FILES["img"]},
                data=form.data,
            )

        else:
            messages.error(request, "Invalid input!")

    address = "http://127.0.0.1:8000/api/getall"

    myProds = requests.get(
        address, headers={"Authorization": "Bearer " + request.session["jwt"]}
    ).json()
    # print(myProds)
    return render(
        request, "manage_products.html", {"products": myProds, "form": myform}
    )
