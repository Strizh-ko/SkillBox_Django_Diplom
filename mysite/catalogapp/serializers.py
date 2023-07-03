from rest_framework import serializers
from .models import Category


class SubCategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id",
            "title",
            "image",
        )

    def get_image(self, instance: Category) -> dict[str]:
        try:
            image = instance.category_img.all()[0]
            return {"src": image.src(), "alt": image.alt()}
        except IndexError:
            return {}


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = SubCategorySerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Category
        fields = ("id", "title", "image", "subcategories")

    def get_image(self, instance: Category) -> dict[str]:
        try:
            image = instance.category_img.all()[0]
            return {"src": image.src(), "alt": image.alt()}
        except IndexError:
            return {}
