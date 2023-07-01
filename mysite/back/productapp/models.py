from django.db import models
from catalogapp.models import Category


def product_path(instance: 'ProductImage', filename: str) -> str:
    return 'products/images/id_{pk}/{file}'.format(
        pk=instance.product.pk,
        file=filename
    )


class Product(models.Model):
    title = models.CharField(max_length=128, blank=False, null=False, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    count = models.IntegerField(blank=False, null=False, verbose_name='Количество')
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    description = models.CharField(max_length=64, blank=True, null=False, verbose_name='Краткое описание')
    fullDescription = models.TextField(blank=True, null=False, verbose_name='Полное описание')
    freeDelivery = models.BooleanField(default=False, verbose_name='Бесплатная доставка')
    rating = models.IntegerField(blank=False, null=False, verbose_name='Количество звёзд')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 related_name='products', verbose_name='Категория')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('pk',)

    def __str__(self):
        return self.title


class ProductSpecification(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False, verbose_name='Характеристика')
    value = models.CharField(max_length=256, blank=False, null=False, verbose_name='Значение')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
                                related_name='specification', verbose_name='Товар')

    class Meta:
        verbose_name = 'Техническая характеристика'
        verbose_name_plural = 'Технические характеристики'
        ordering = ('pk',)

    def __str__(self):
        return self.name


class SaleProduct(models.Model):
    salePrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена со скидкой')
    dateFrom = models.DateField(auto_now_add=True, verbose_name='Дата начала акции')
    dateTo = models.DateField(blank=True, verbose_name='Дата окончании акции')
    product: Product = models.OneToOneField(Product, on_delete=models.CASCADE,
                                   related_name='sale', verbose_name='Товар')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
        ordering = ('pk',)

    def price(self):
        return self.product.price

    def title(self):
        return self.product.title

    def __str__(self):
        return '{product} теперь стоит {sale}.'.format(
            product=self.product.title,
            sale=self.salePrice
        )


class Tag(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, verbose_name='Название')
    product = models.ManyToManyField(Product, related_name='tags', verbose_name='Товар')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('pk',)

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.CharField(max_length=128, blank=False, null=False, verbose_name='Автор')
    email = models.EmailField(max_length=64, blank=False, null=False, verbose_name='Email-адрес')
    text = models.TextField(default='', blank=True, null=False, verbose_name='Отзыв')
    rate = models.IntegerField(blank=False, null=False, verbose_name='Оценка')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата написания')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='review', verbose_name='Товар')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pk',)

    def __str__(self):
        return self.author


class ProductImage(models.Model):
    image = models.ImageField(upload_to=product_path, default='', null=False, verbose_name='Изображение')
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='product_img', verbose_name='Товар')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ('pk',)

    def src(self):
        return '/media/{product_image_path}'.format(
            product_image_path=self.image
        )

    def alt(self):
        return self.product.title

    def __str__(self):
        return '#{pk} {product}'.format(
            pk=self.product.pk,
            product=self.product.title,
        )






