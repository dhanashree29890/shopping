from django.urls import path

from . import views

urlpatterns = [
    path("getall", views.getall.as_view(), name="getall"),
    path("getone/<int:id>", views.getone.as_view(), name="getone"),  # send get request
    path("create", views.getone.as_view(), name="create"),  # send post req
    path("update/<str:id>", views.updateone.as_view(), name="update"),
    path(
        "delete/<int:id>", views.getone.as_view(), name="delete"
    ),  # send delete requset
]
