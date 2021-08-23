from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from products.models import Products
from .serializers import ProductSerializer, ProductUpdateSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect
from rest_framework.parsers import MultiPartParser


class getall(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        prods = Products.objects.all()
        serializer = ProductSerializer(prods, many=True)
        return Response(serializer.data)


class getone(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        id = id
        try:
            prod = Products.objects.get(id=id)
            serializer = ProductSerializer(prod, many=False)
            return Response(serializer.data)
        except:
            return Response("Item does not exist")

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            result = " is valid"
            serializer.save()
        else:
            result = " not valid"

        return Response(result)

    def delete(self, request, id, format=None):
        id = id
        try:
            prod = Products.objects.get(id=id)
            prod.delete()
            return Response("deleted")
        except:
            return Response("Item not found")


class updateone(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "update_prod.html"
    parser_classes = (MultiPartParser,)

    # permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        id = id
        try:
            prod = Products.objects.get(id=id)
            serializer = ProductUpdateSerializer(prod, many=False)

            return Response(
                {"serializer": serializer, "prod": prod}
            )  # serializer.data)
        except:
            return Response("Item does not exist")

    def post(self, request, id, format=None):

        prod = Products.objects.get(id=id)
        print("files recieved are ", request.data["img"])
        if request.data["img"] == "":
            mydict = {
                "name": request.data["name"],
                "img": prod.img,
                "cost": request.data["cost"],
                "quantity": request.data["quantity"],
                "is_active": request.data["is_active"],
            }
            serializer = ProductUpdateSerializer(prod, data=mydict, partial=True)
        else:
            serializer = ProductUpdateSerializer(prod, data=request.data, partial=True)

        if not serializer.is_valid():
            print("serializer is not valid")
            print(serializer.errors)
            return Response({"serializer": serializer, "prod": prod})
        serializer.save()
        return redirect("/products/manage_products/" + str(prod.seller.id))

    # def post(self, request, id):
    #     id = int(id)
    #     prod = Products.objects.get(id=id)
    #     print("my req data is ", request.data)
    #     serializer = ProductUpdateSerializer(
    #         instance=prod, data=request.data, partial=True
    #     )

    #     if serializer.is_valid():
    #         serializer.save()
    #         result = " is valid"
    #     else:
    #         result = " not valid"
    #         print("not valid")
    #         return Response(serializer.errors)

    #     return Response(result)
