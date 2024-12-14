from django.contrib import admin

# Register your models here.
from .models import Supplier, Category, Product, Sale, InventoryMovement
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'contact_email', 'contact_phone')
    search_fields = ('name', 'contact_name')
    list_filter = ('contact_name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name')
    search_fields = ('name', 'display_name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity_in_stock', 'category', 'supplier', 'created_at', 'updated_at')
    list_filter = ('category', 'supplier', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'quantity', 'total_price', 'date')
    list_filter = ('date', 'product', 'customer')
    search_fields = ('product__name', 'customer__username')
    date_hierarchy = 'date'


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'date', 'description')
    list_filter = ('movement_type', 'date', 'product')
    search_fields = ('product__name', 'description')
    date_hierarchy = 'date'