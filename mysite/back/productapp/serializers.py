from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Tag, Review, Product, SaleProduct
from datetime import datetime


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ('product',)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, required=False)
    specifications = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'category', 'price', 'count', 'date', 'title',
                  'description', 'fullDescription', 'freeDelivery', 'images', 'tags', 'reviews',
                  'specifications', 'rating')

    def get_reviews(self, instance: Product) -> list[dict]:
        return [{'author': review.author, 'email': review.email,
                 'text': review.text, 'rate': review.rate,
                 'date': datetime.strftime(review.date, '%d-%m-%Y %H:%M')}
                for review in instance.review.all()]

    def get_specifications(self, instance: Product) -> list[dict]:
        return [{'name': specification.name, 'value': specification.value}
                for specification in instance.specification.all()]

    def get_images(self, instance: Product) -> list[dict]:
        return [{'src': image.src(), 'alt': image.alt()} for image in instance.product_img.all()]

    def get_price(self, instance: Product):
        try:
            return instance.sale.salePrice
        except ObjectDoesNotExist:
            return instance.price


class ShortInfoProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, required=False)
    images = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id', 'category', 'price',
            'count', 'date', 'title',
            'description', 'freeDelivery',
            'images', 'tags', 'reviews', 'rating'
        )

    def get_reviews(self, instance: Product) -> int:
        return len(instance.review.all())

    def get_images(self, instance: Product) -> list[dict]:
        return [{'src': image.src(), 'alt': image.alt()} for image in instance.product_img.all()]

    def get_price(self, instance: Product):
        try:
            return instance.sale.salePrice
        except ObjectDoesNotExist:
            return instance.price


class SaleProductSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    dateFrom = serializers.DateField(format='%d-%m')
    dateTo = serializers.DateField(format='%d-%m')
    price = serializers.StringRelatedField()
    title = serializers.StringRelatedField()

    class Meta:
        model = SaleProduct
        fields = ('id', 'price', 'salePrice',
                  'dateFrom', 'dateTo', 'title',
                  'images')

    def get_id(self, instance: SaleProduct) -> Product.pk:
        return instance.product.pk

    def get_images(self, instance: SaleProduct) -> list[dict]:
        return [{'src': image.src(), 'alt': image.alt()} for image in instance.product.product_img.all()]











