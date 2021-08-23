from rest_framework import serializers

from products.models import Products


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            "name",
            "img",
            "cost",
            "quantity",
            "is_active",
            "seller",
            "id",
        ]  # "__all__"  #


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            "name",
            "img",
            "cost",
            "quantity",
            "is_active",
        ]  # "__all__"  #
