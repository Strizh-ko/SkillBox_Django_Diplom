from django.contrib import admin
from .models import Product, ProductImage, ProductSpecification, SaleProduct, Tag, Review


class ProductSpecificationInline(admin.StackedInline):
    model = ProductSpecification


class TagInline(admin.StackedInline):
    model = Product.tags.through


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
        TagInline,
        ProductImageInline,
    ]

    list_display = ('pk', 'title', 'price', 'count',
                    'date', 'description',
                    'freeDelivery', 'rating', 'category')

    list_editable = ('freeDelivery',)

    list_display_links = ('pk', 'title')
    ordering = ('pk',)

    def description_short(self, obj: Product) -> str:
        if len(obj.fullDescription) < 50:
            return obj.fullDescription
        return obj.fullDescription[:50] + "..."


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_display_links = ('pk', 'name')
    ordering = ('pk',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'email', 'text', 'rate', 'date', 'product')
    list_display_links = ('pk', 'author')
    ordering = ('pk',)


@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'salePrice', 'dateFrom', 'dateTo', 'product')
    list_display_links = ('pk',)
    ordering = ('pk',)


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'value', 'product')
    list_display_links = ('pk', 'name')
    ordering = ('pk',)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'image', 'product')
    list_display_links = ('pk',)
    ordering = ('pk',)





