from rest_framework import generics
from .models import Date
from .serializers import DateSerializer
import uuid
from django.conf import settings
from yookassa import Payment
from yookassa import Configuration
from django.shortcuts import HttpResponse

class DateListAPIView(generics.ListAPIView):
    queryset = Date.objects.all()
    serializer_class = DateSerializer



# Устанавливаем идентификаторы
Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

def create_payment(amount, return_url):
    payment = Payment.create({
        "amount": {
            "value": str(amount),  # Сумма платежа в рублях
            "currency": "RUB"
        },
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": return_url  # Куда перенаправить пользователя после оплаты
        },
        "description": "Оплата заказа",
        "metadata": {
            "order_id": str(uuid.uuid4())  # Уникальный идентификатор заказа
        }
    })
    return payment.confirmation.confirmation_url


def create_payment_view(request):
    amount = request.GET.get("amount", 1000)  # Можно передавать сумму через параметры
    return_url = "https://example.com/success"  # Укажи свой URL возврата
    payment_url = create_payment(amount, return_url)
    return HttpResponse(payment_url)