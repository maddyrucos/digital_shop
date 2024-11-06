from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.utils.representation import serializer_repr
from django.shortcuts import get_object_or_404
from django.db.models import Q

from shop.models import Product, Content, Sale, User
from shop.services import purchase
from api.serializers import ProductSerializer, ContentSerializer, SaleSerializer


@api_view(['GET'])
def api_products(request):
    if request.method == 'GET':
        q = (Q(is_active=True) & Q(content__isnull=False))
        products = Product.objects.filter(q)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response(request, status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def api_products_detail(request, product_id):
    event = Product.objects.get(product_id)
    if request.method == 'GET':
        serializer = ProductSerializer(event)
        return Response(serializer.data)
    else:
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def api_sales(request):
    if request.method == 'GET':
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)
    else:
        return Response(request, status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def api_sales_detail(request, sale_id):
    sales = Sale.objects.get(sale_id)
    if request.method == 'GET':
        serializer = SaleSerializer(sales)
        return Response(serializer.data)
    else:
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def api_content(request):
    if request.method == 'GET':
        content = Content.objects.all()
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)
    else:
        return Response(request, status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def api_content_detail(request, content: str):
    content = Product.objects.get(content)
    if request.method == 'GET':
        serializer = Content(content)
        return Response(serializer.data)
    else:
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def api_product_buy(request, product_id: int):
    user = get_object_or_404(User, username=request.user)
    product = get_object_or_404(Product, pk=product_id)
    if user.userprofile.balance >= product.price:
        sale = purchase.buy_from_balance(user, product)
        serializer = SaleSerializer(sale)
        return Response(serializer.data)
    else:
        return Response(status=HTTP_204_NO_CONTENT)