from django.contrib import admin
from .models import Category, ImageCategory


class CategoryInline(admin.StackedInline):
    model = ImageCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]
    list_display = ("pk", "title", "parent", "main")
    list_display_links = ("pk", "title")
    list_editable = ("main",)
    ordering = ("pk",)


@admin.register(ImageCategory)
class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "image", "category")
    list_display_links = ("pk",)
    ordering = ("pk",)
