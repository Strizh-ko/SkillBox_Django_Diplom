from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def product_list(request):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product/list.html',
                  {
                      'category': category,
                      'categories': categories,
                      'products': products
                  })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})