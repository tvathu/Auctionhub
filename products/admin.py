from django.contrib import admin
from .models import Product, Category

admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'starting_price', 'is_active', 'created_at']
    list_filter = ['is_active', 'category']
    search_fields = ['title', 'seller__username']