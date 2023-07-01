from rest_framework.exceptions import ValidationError
from datetime import datetime
import statistics
from usersapp.models import ProfileUser
from .models import Review
from .models import Product


def setup_average_rating(product_pk: Product.pk) -> int:
    return statistics.mean(review.rate
                           for review in Review.objects.only('rate').filter(product_id=product_pk)
                           )


def get_valid_review_data(request_data: dict, user: ProfileUser, product: Product) -> dict:
    return {
        'date': datetime.now().strftime('%d-%m-%Y %H:%M'),
        'author': user.fullName,
        'text': request_data.get('text', ''),
        'rate': request_data.get('rate', 1),
        'email': user.email,
        'product': product.pk,
    }


def create_review(valid_data: dict, product: Product):
    Review.objects.create(author=valid_data.get('author', 'Неизвестно'),
                          email=valid_data.get('email', 'unknow@mai.ru'),
                          text=valid_data.get('text', ''),
                          rate=valid_data.get('rate', 1),
                          date=valid_data.get('date'),
                          product_id=product.pk)


def user_review_exists(email: str, product_id: Product.pk):
    if Review.objects.filter(email=email, product_id=product_id).exists():
        raise ValidationError('Комментарий на товар уже был оставлен этим пользователем.')




