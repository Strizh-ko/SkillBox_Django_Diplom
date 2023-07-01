from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from django.db.models.query import QuerySet
from basketapp.basket import Basket
from productapp.models import Product
from usersapp.utils import validate_fullname_user
from .models import Order, QuantityProductsInBasket
from decimal import Decimal
from datetime import datetime


def get_nice_data(date: datetime) -> str:
    return datetime.strftime(date, '%d %B %Y, %H:%M:%S')


def get_order_user_or_400(request: Request, pk: Order.pk, payment: bool = False) -> Order:
    if not payment:
        order = Order.objects.select_related('user_profile').prefetch_related(
                'products').filter(id=pk, user_profile_id=request.user.pk).first()
    else:
        order = Order.objects.select_related('user_profile').prefetch_related(
                'products').filter(id=pk, user_profile_id=request.user.pk, status='unconfirmed').first()
        if order and not all([order.fullName, order.email, order.phone, order.deliveryType,
                              order.paymentType, order.city, order.address]):
            raise ValidationError('Заказ содержит не все данные.')

    if not order:
        raise ValidationError('Заказ не принадлежит этому пользователю, или не существует, или уже оплачен.')
    return order


def get_detail_order_data(order_data: dict) -> tuple:
    data_order = tuple(order_data.get(info)
                       for info in ['fullName', 'email', 'phone', 'deliveryType', 'paymentType', 'city', 'address'])
    if all(data_order):
        return data_order
    raise ValidationError('Не все данные заполены корректно.')


def get_detail_payment_data(payment_data: dict) -> tuple:
    return tuple(payment_data.get(info) for info in ['number', 'name', 'month', 'year', 'code'])


def save_number_products_in_basket(order_pk: Order.pk, products: QuerySet, bk: Basket):
    for product in products:
        QuantityProductsInBasket.objects.create(
            order_id=order_pk,
            product_id=product.pk,
            quantity=bk.get_count_product_in_basket(product_pk=product.pk)
        )


def setup_order(order: Order, params: tuple):
    if order.status != 'unconfirmed':
        raise ValidationError('Заказ уже оплачен.')
    order.fullName, order.email, order.phone, order.deliveryType, order.paymentType, order.city, order.address = params


def setup_count_products_in_basket(order_pk: Order.pk, data: dict):
    for index in range(len(data.get('products', list()))):
        product_info: QuantityProductsInBasket = QuantityProductsInBasket.objects.filter(
            order_id=order_pk,
            product_id=data['products'][index]['id']
        ).first()

        data['products'][index]['count'] = product_info.quantity


def remove_goods_from_warehouse(order: Order, bk: Basket):
    for item in order.products.all():
        product = Product.objects.get(id=item.pk)
        product.count -= bk.get_count_product_in_basket(product_pk=product.pk)
        product.save()


def check_delivery_type_and_price_setting(order: Order):
    if order.deliveryType == 'express':
        order.totalCost += Decimal(500)
    else:
        if order.totalCost < 2000:
            order.totalCost += Decimal(200)


def validation_all_data(name: str, number: str, month: str, year: str, code: str):
    if not all(data.isdigit() for data in [number, month, year, code]):
        raise ValidationError('Даты и данные карты должны быть числом')

    if int(month) not in range(1, 13):
        raise ValidationError('Месяц должен быть в пределах от 1 до 12.')

    if int(year) not in range(1970, 2200):
        raise ValidationError('Невалидный год.')

    if int(number) % 2 != 0:
        raise ValidationError('Номер карты должен быть четным.')

    if len(number) > 8:
        raise ValidationError('Номер карты не должен быть длиннее 8 цифр.')

    if number[-1] == '0':
        raise ValidationError('Номер карты не должен заканчиваться на ноль.')

    if len(code) != 3:
        raise ValidationError('CVV-код должен быть трезначным.')

    validate_fullname_user(fullname=name)


