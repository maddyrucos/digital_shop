from rest_framework import serializers, viewsets
from shop.models import Product, Content, Sale

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'