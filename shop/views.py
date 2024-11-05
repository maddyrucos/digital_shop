from http.client import HTTPResponse
from unicodedata import category

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q

from shop.models import *


def index(request):
    q = (Q(is_active=True) & Q(content__isnull=False))
    products = Product.objects.filter(q).order_by('date_added')[:10]
    context = {'last_products': products }
    return render(request, 'shop/index.html', context=context)


def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = { 'product': product }
    return render(request, 'shop/product_page.html', context=context)


@login_required()
def product_buy(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    content = get_object_or_404(Content, product=product_id)
    if request.user.userprofile.balance > product.price:
        user = get_object_or_404(User, username=request.user)
        user.userprofile.balance -= product.price
        user.userprofile.save()
        data = content.data
        if not content.is_unlimited:
            content.delete()
        context = { 'product': product.name, 'user': user.userprofile.balance, 'content': data }
        return JsonResponse(context)
    else:
        return JsonResponse({ 'price': product.price, 'balance': request.user.userprofile.balance })


def catalog(request):
    categories = Category.objects.filter(parent=None)
    return render(request, 'shop/catalog.html', { 'categories': categories })


def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    subcategories = category.children.all()
    return render(request, 'shop/category.html', {'category': category, 'products': products, 'subcategories': subcategories, 'user': request.user })

def search(request):
    query=request.GET.get('q')
    results = Product.objects.filter(name__icontains=query).values('id', 'name', 'cost')
    return JsonResponse({'results': list(results)})


@login_required
def profile(request):
    return render(request, 'shop/profile.html')