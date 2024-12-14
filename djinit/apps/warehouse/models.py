from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        return self.display_name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Sale(models.Model):
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sale of {self.product.name} on {self.date}"


class InventoryMovement(models.Model):
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=20, choices=[
        ('purchase', 'Compra'),
        ('sale', 'Venta'),
        ('return', 'Devolución'),
    ])
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movement_type} of {self.product.name} on {self.date}"

