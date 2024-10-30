from django.urls import path
from shop import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>', views.category, name='category'),
    path('catalog/', views.catalog, name='catalog'),
    path('products/<int:product_id>', views.product, name='product'),
    path('products/<int:product_id>/buy', views.product_buy, name='buy_product'),
    path('contacts/', views.index, name='contacts'),
    path('search/', views.search, name='search')
]