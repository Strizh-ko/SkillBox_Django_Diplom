from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name', 'price']

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100, db_index=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    description = models.TextField(max_length=1000, null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    # discount = models.PositiveSmallIntegerField(default=0)
    # created_by = models.ForeignKey(User, on_delete=models.PROTECT)



