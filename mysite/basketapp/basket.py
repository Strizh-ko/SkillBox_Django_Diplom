from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist

from mysite import settings
from productapp.models import Product
from rest_framework.request import Request


class Basket:
    def __init__(self, request: Request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = dict()
        self.cart = cart

    def add(self, product: Product, count: int = 1):
        product_id = str(product.pk)
        try:
            price = product.sale.salePrice
        except ObjectDoesNotExist:
            price = product.price
        if product_id not in self.cart:
            self.cart[product_id] = {
                "count": count,
                "price": str(price),
            }
        else:
            self.cart[product_id]["count"] += count
        self.save()

    def delete(self, product: Product, count: int = 1):
        product_id = str(product.pk)
        if count >= self.cart[product_id]["count"]:
            del self.cart[product_id]
        else:
            self.cart[product_id]["count"] -= count

        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_price(self) -> Decimal:
        return sum(
            data_many.get("count", 0) * Decimal(data_many.get("price", 0))
            for data_many in self.cart.values()
        )

    def get_count_product_in_basket(self, product_pk) -> int:
        product_id = str(product_pk)
        return self.cart.get(product_id, {}).get("count", 0)

    def get_price_product_in_basket(self, product_pk) -> Decimal:
        product_id = str(product_pk)
        return Decimal(self.cart.get(product_id, {}).get("price", 0))
