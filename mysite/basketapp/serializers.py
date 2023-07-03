from rest_framework import serializers
from productapp.models import Product
from productapp.serializers import TagSerializer


class BasketSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    reviews = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        )

    def get_count(self, instance: Product) -> int:
        return self.context.get_count_product_in_basket(product_pk=instance.pk)

    def get_price(self, instance: Product) -> int:
        return self.context.get_price_product_in_basket(product_pk=instance.pk)

    def get_reviews(self, instance: Product) -> int:
        return len(instance.review.all())

    def get_images(self, instance: Product) -> list[dict]:
        return [
            {"src": image.src(), "alt": image.alt()}
            for image in instance.product_img.all()
        ]
