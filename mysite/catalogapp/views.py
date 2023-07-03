from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from productapp.models import Product
from productapp.serializers import ShortInfoProductSerializer
from .models import Category
from .serializers import CategorySerializer
from .utils import main_filter


class CategoryListApiView(ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BannersListApiView(ListAPIView):
    queryset: Product = (
        Product.objects.prefetch_related(
            "review",
            "product_img",
            "tags",
        )
        .select_related("category")
        .filter(category__main=True)
    )
    serializer_class = ShortInfoProductSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CatalogApiView(APIView):
    def get(self, request: Request) -> Response:
        return Response(
            {"items": ShortInfoProductSerializer(main_filter(request), many=True).data}
        )
