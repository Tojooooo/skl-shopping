# products/models.py
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, default="default")
    password = models.CharField(max_length=50, default="none")
    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} - {self.product.name}"
    
class Comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    content = models.TextField()
    type =  models.IntegerField(default=1)

    def __str__(self):
        return f"Comment {self.product.name} {self.content}"