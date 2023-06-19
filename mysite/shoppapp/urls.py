from django.urls import path
from . import views

app_name = 'shoppapp'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category', views.product_list, name='product_list_by_category'),
    path('<int:id>', views.product_detail, name='product_detail'),
]