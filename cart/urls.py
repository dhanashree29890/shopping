from django.urls import path

from . import views

urlpatterns = [
    path("<str:ip>", views.cart, name="cart"),
    path("ajax_url/", views.update_quant, name="ajax_url"),
]
