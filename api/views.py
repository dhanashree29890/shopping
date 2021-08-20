from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from products.models import Products
from .serializers import ProductSerializer


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

    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        id = int(id)
        prod = Products.objects.get(id=id)
        print(request.data)
        serializer = ProductSerializer(instance=prod, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            result = " is valid"

        else:
            result = " not valid"
            print("not valid")
            return Response(serializer.errors)

        return Response(result)
