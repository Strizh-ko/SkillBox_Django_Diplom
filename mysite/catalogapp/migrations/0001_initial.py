# Generated by Django 4.2.1 on 2023-06-28 16:13

import catalogapp.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=64, verbose_name="Название категории"),
                ),
                (
                    "main",
                    models.BooleanField(
                        default=False, verbose_name="Избранная категория"
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subcategories",
                        to="catalogapp.category",
                        verbose_name="Подкатегории",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "ordering": ("pk",),
            },
        ),
        migrations.CreateModel(
            name="ImageCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        default="",
                        upload_to=catalogapp.models.category_path,
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category_img",
                        to="catalogapp.category",
                        verbose_name="Категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение категории",
                "verbose_name_plural": "Изображения категорий",
                "ordering": ("pk",),
            },
        ),
    ]
