from django.contrib import admin
from .models import User, Product, Payment

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Payment)