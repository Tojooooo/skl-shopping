# products/models.py
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return f"Payment {self.id} - {self.product.name}"