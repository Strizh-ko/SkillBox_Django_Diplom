from django.db.models import Count
from productapp.models import Product
from rest_framework.request import Request
from django.db.models.query import QuerySet


def get_query_params(request: Request) -> tuple:
    full_body_request = request.query_params
    return full_body_request.get(
        'filter[name]', ''
    ), full_body_request.get(
        'filter[minPrice]'
    ), full_body_request.get(
        'filter[maxPrice]'
    ), full_body_request.get(
        'filter[freeDelivery]'
    ) == 'true', full_body_request.get(
        'filter[available]'
    ) == 'true', full_body_request.getlist(
        'tags[]'
    ), request.META.get('HTTP_REFERER', '').split(
        '?filter='
    ), full_body_request.get(
        'sort', ''
    ), full_body_request.get('sortType', '')


def sort_desired_products(products: QuerySet, sort: str, type_sort: str):
    type_sort = '-' if type_sort == 'inc' else ''
    if sort == 'reviews':
        return products.annotate(quantity_review=Count('review')).order_by('{type_sort}quantity_review'.format(
            type_sort=type_sort
        ))
    return products.order_by('{type_sort}{sort}'.format(
        type_sort=type_sort,
        sort=sort
    ))


def filter_category(category: list[str], products: QuerySet):
    if len(category) == 2:
        return products.filter(category__title=' '.join(category[-1].split('%20')))

    path, digit = category[0].split('catalog/')
    if digit:
        return products.filter(category__id=int(digit[:-1]))
    return products


def main_filter(request):
    title, min_price, max_price, free_del, available, tags, category, sort, type_sort = get_query_params(request=request)
    desired_products = Product.objects.prefetch_related(
        'review', 'product_img', 'tags').select_related('category').filter(
        price__range=(min_price, max_price))

    if free_del:
        desired_products = desired_products.filter(freeDelivery=free_del)

    if title:
        desired_products = desired_products.filter(title__icontains=title.title())

    if available:
        desired_products = desired_products.exclude(count=0)

    if tags:
        for tag in tags:
            desired_products = desired_products.filter(tags__id=tag)

    desired_products = filter_category(category=category, products=desired_products)

    return sort_desired_products(products=desired_products, sort=sort, type_sort=type_sort)
