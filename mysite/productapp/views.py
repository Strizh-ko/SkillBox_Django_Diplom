from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .models import Tag, Product, SaleProduct
from django.db.models import Count
from .serializers import (TagSerializer, ReviewSerializer, ProductDetailSerializer,
                          SaleProductSerializer, ShortInfoProductSerializer)

from usersapp.models import ProfileUser
from .utils import setup_average_rating, get_valid_review_data, create_review, user_review_exists
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class TagsListApiView(ListAPIView):
    queryset = Tag.objects.only('pk', 'name').all()
    serializer_class = TagSerializer

    def get(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductDetailApiView(RetrieveAPIView):
    queryset = Product.objects.prefetch_related(
        'review', 'specification', 'product_img', 'tags').select_related('category').all()
    serializer_class = ProductDetailSerializer


class SaleListApiView(ListAPIView):
    queryset: SaleProduct = SaleProduct.objects.prefetch_related('product').all()
    serializer_class = SaleProductSerializer

    def list(self, request: Request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['items'] = response.data.pop('results')
        return response


class ProductLimitedListApiView(ListAPIView):
    queryset: Product = Product.objects.prefetch_related(
        'review', 'product_img', 'tags').select_related('category').filter(count=0)[:16]
    serializer_class = ShortInfoProductSerializer

    def get(self, request: Request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductPopularListApiView(ListAPIView):
    queryset: Product = Product.objects.prefetch_related(
        'review', 'product_img', 'tags').select_related('category').annotate(
        quantity_purchases=Count('review')
    ).order_by(
        '-quantity_purchases'
    ).exclude(count=0)[:8]
    serializer_class = ShortInfoProductSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateProductReviewApiView(CreateAPIView):
    queryset = Product.objects.only('pk', 'rating').prefetch_related('review')

    serializer_class = ReviewSerializer
    lookup_url_kwarg = "pk"
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user: ProfileUser = ProfileUser.objects.get(id=request.user.pk)
        product: Product = self.get_object()

        valid_review_data = get_valid_review_data(request_data=request.data, user=user, product=product)
        user_review_exists(email=valid_review_data.get('email'), product_id=valid_review_data.get('product'))

        review_serializer: ReviewSerializer = self.get_serializer(data=valid_review_data)
        review_serializer.is_valid(raise_exception=True)
        create_review(valid_data=valid_review_data, product=product)

        product.rating = setup_average_rating(product_pk=product.pk)
        product.save()
        return Response(status=status.HTTP_201_CREATED)












