from rest_framework import serializers
from productapp.serializers import ShortInfoProductSerializer
from .models import Order
from .utils import get_nice_data


class OrderSerializer(serializers.ModelSerializer):
    createdAt = serializers.SerializerMethodField()
    orderId = serializers.SerializerMethodField()
    fullName = serializers.StringRelatedField()
    email = serializers.StringRelatedField()
    phone = serializers.StringRelatedField()
    products = ShortInfoProductSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ('id', 'createdAt', 'fullName', 'email',
                  'phone', 'deliveryType', 'paymentType', 'totalCost',
                  'status', 'city', 'address', 'products', 'orderId')

    def get_createdAt(self, instance: Order) -> str:
        return get_nice_data(date=instance.createdAt)

    def get_orderId(self, instance: Order) -> Order.pk:
        return instance.pk




