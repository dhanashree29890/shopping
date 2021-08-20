from django.urls import path

from . import views

urlpatterns = [
    path("manage_products/<int:id>", views.manage_products, name="manage_products"),
    # path("getone/<int:id>", views.getone, name="getone"),
    path("delete_prod/<int:id>/<int:seller_id>", views.delete_prod, name="delete_prod"),
    path("update_prod/<int:id>", views.update_prod, name="update_prod"),
]
