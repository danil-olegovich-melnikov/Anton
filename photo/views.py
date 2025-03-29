from rest_framework import generics
from .models import Date, Photo, Payment, Order, Client
from .serializers import DateSerializer
import uuid
from django.conf import settings
from yookassa import Payment as Ypayment
from yookassa import Configuration
from django.shortcuts import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


class DateListAPIView(generics.ListAPIView):
    queryset = Date.objects.all()
    serializer_class = DateSerializer



# Устанавливаем идентификаторы
Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

def create_payment(amount, return_url, email):
    payment = Ypayment.create({
        "amount": {
            "value": str(amount),
            "currency": "RUB"
        },
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": return_url
        },
        "description": f"Оплата заказа: {email}",
        "metadata": {
            "order_id": str(uuid.uuid4())
        }
    })
    return payment.confirmation.confirmation_url


def create_payment_view(request):
    amount = request.GET.get("amount", 1000)
    return_url = request.GET.get("return_url", "https://example.com/success")
    email = request.GET.get("email", "")
    pk_photos = request.GET.get("photos", "")

    print(pk_photos)
    if not amount:
        return HttpResponse('Не указана сумма')
    elif not email:
        return HttpResponse('Почта не указана')
    elif not pk_photos:
        return HttpResponse('Не указаны фотографии')
    
    price = 0
    photos = []
    for pk in pk_photos.split(','):
        if Photo.objects.filter(id=pk).exists():
            photo = Photo.objects.get(id=pk)
            photos.append(photo)
            price += photo.price
        else:
            return HttpResponse('Фотографии не существует')

    print(price)
    if price != int(amount):
        return HttpResponse(f'Не правильно указана сумма, должно быть {price} рублей')

    client = Client.objects.get_or_create(email=email)[0]
    payment_url = create_payment(amount, return_url, email)
    payment = Payment.objects.create(client=client, url=payment_url)
    for photo in photos:
        Order.objects.create(payment=payment, photo=photo)

    return HttpResponse(payment_url)


@csrf_exempt
def payment_webhook(request):
    payload = json.loads(request.body)
    if payload.get("event") == "payment.succeeded":
        order_id = payload["object"]["metadata"]["order_id"]
        print(f"Платёж прошел успешно! Order ID: {order_id}")
    return JsonResponse({"status": "ok"})