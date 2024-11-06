from itertools import count

from shop.models import UserProfile, Product, Content, Sale
from django.shortcuts import get_object_or_404


def buy_from_balance(user: UserProfile, product: Product, count=1) -> Sale:
    content = product.content.all()[0]
    user.userprofile.balance -= product.price
    user.userprofile.save()
    data = content.data
    if not content.is_unlimited:
        content.delete()
    sale = Sale.objects.create(
        customer=user,
        product=product,
        count=count,
        total_cost=product.price*count,
        status='paid',
        content=data,
    )
    return sale
