from unicodedata import category

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from shop.models import *


def index(request):
    products = Product.objects.filter(is_active=True).order_by('date_added')[:10]
    context = {'last_products': products}
    return render(request, 'shop/index.html', context=context)


def product(request, product_id):

    return render(request, 'shop/product_page.html')


@login_required()
def product_buy(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = get_object_or_404(User, username=request.user)
    content = Product.successful_payment_answer.first()
    context = { 'product': product, 'user': user, 'content': content }
    return JsonResponse(context)


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