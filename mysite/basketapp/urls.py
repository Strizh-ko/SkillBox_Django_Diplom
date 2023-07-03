from django.urls import path
from .views import BasketApiView

app_name = "basketapp"

urlpatterns = [
    path("api/basket", BasketApiView.as_view(), name="basket"),
]
