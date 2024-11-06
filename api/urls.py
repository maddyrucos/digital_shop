from django.urls import path
from api.views import *

app_name='api'

urlpatterns = [
    path('products/', api_products, name='products'),
    path('products/<int:product_id>', api_products_detail, name='product'),
    path('products/<int:product_id>/buy', api_product_buy, name='api_product_buy'),
    path('sales/', api_sales, name='sales'),
    path('sales/<int:sale_id>', api_sales_detail, name='sale'),
    path('content/', api_content, name='content'),
    path('content/<int:product_id>', api_content_detail, name='content'),
]