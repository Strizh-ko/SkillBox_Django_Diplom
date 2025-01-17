# Generated by Django 4.2.1 on 2023-07-01 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("productapp", "0002_alter_productspecification_value"),
        ("usersapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                    "createdAt",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "deliveryType",
                    models.CharField(
                        blank=True, max_length=32, verbose_name="Тип доставки"
                    ),
                ),
                (
                    "paymentType",
                    models.CharField(
                        blank=True, max_length=32, verbose_name="Тип оплаты"
                    ),
                ),
                (
                    "totalCost",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Цена заказа"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True, max_length=32, verbose_name="Статус оплаты"
                    ),
                ),
                (
                    "city",
                    models.CharField(blank=True, max_length=64, verbose_name="Город"),
                ),
                (
                    "address",
                    models.CharField(blank=True, max_length=128, verbose_name="Адрес"),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        related_name="orders",
                        to="productapp.product",
                        verbose_name="Товары",
                    ),
                ),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="orders",
                        to="usersapp.profileuser",
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заказ",
                "verbose_name_plural": "Заказы",
                "ordering": ("pk",),
            },
        ),
        migrations.CreateModel(
            name="QuantityProductsInBasket",
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
                ("quantity", models.IntegerField()),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="orderapp.order"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="productapp.product",
                    ),
                ),
            ],
        ),
    ]
