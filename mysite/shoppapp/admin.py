from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        # 'slug',
    ]
    # prepopulated_fields = {'slug': ('name', )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        # 'slug',
        'description',
        # 'description_short',
        'available',
        'price',
        # 'discount',
        'created_at',
        'archived',
        # 'updated_at',
    ]


    list_filter = [
        'available',
        'created_at',
        # 'updated_at',
    ]

    list_editable = [
        'price',
        # 'discount',
        'available',
        'archived'
    ]
