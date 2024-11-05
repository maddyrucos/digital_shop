from django.contrib import admin
from .models import *

models_list = [
    UserProfile,
    Product,
    Content,
    Category,
    Payment,
    Sale,
   ]

for model in models_list:
    admin.site.register(model)
