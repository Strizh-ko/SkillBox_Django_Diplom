from rest_framework.exceptions import ValidationError
from productapp.models import Product
from .serializers import BasketSerializer
from .basket import Basket


def get_serialized_data(basket: Basket) -> BasketSerializer.data:
    return BasketSerializer(Product.objects.prefetch_related(
        'review', 'product_img', 'tags').select_related('category').filter(pk__in=basket.cart.keys()),
                                      many=True, context=basket).data


def check_user_input_count(request_data: dict, product: Product, bk: Basket) -> int | ValidationError:
    quantity_products_user = int(request_data.get('count', 0))
    if quantity_products_user < 1:
        raise ValidationError('Количество запрашиваемых товаров должно быть больше нуля.')

    if bk.cart.get(str(product.pk), {}).get('count', 0) + quantity_products_user > product.count:
        raise ValidationError('Количество товаров на складе меньше запрашиваемого.')

    return quantity_products_user