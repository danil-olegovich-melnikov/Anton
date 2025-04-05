from rest_framework import generics
from .models import Date, Photo, Payment, Order, Client
from .serializers import DateSerializer, PaymentSerializer
import uuid
from django.conf import settings
from yookassa import Payment as Ypayment
from yookassa import Configuration
from django.shortcuts import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.shortcuts import redirect

class DateListAPIView(generics.ListAPIView):
    queryset = Date.objects.all()
    serializer_class = DateSerializer



# Устанавливаем идентификаторы
Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def create_payment(host, amount, email):
    order_id = uuid.uuid4()
    payment = Ypayment.create({
        "amount": {
            "value": str(amount),
            "currency": "RUB"
        },
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": f"http://{host}/api/payment_success/{order_id}/"
        },
        "description": f"Оплата заказа: {email}",
        "metadata": {
            "order_id": str(order_id)
        }
    })
    print(f"{host}/api/payment_success/{order_id}/")
    return payment.confirmation.confirmation_url, order_id


def create_payment_view(request):
    amount = request.GET.get("amount", 1000)
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
    payment_url, order_id = create_payment(request.get_host(), amount, email)
    payment = Payment.objects.create(client=client, url=payment_url, order_id=order_id)
    for photo in photos:
        Order.objects.create(payment=payment, photo=photo)

    return HttpResponse(payment_url)


@csrf_exempt
def payment_webhook(request):
    if request.body:   
        payload = json.loads(request.body)
        if payload.get("event") == "payment.succeeded":
            order_id = payload["object"]["metadata"]["order_id"]
            if Payment.objects.filter(order_id == order_id).exists():
                payment = Payment.objects.get(order_id == order_id)
                payment.is_paid = True
                payment.save()
                print(f"Платёж прошел успешно! Order ID: {order_id}")
            else:
                print('Ошибка')
    return JsonResponse({"status": "ok"})


@csrf_exempt
def payment_success(request, order_id):
    print(order_id)
    if Payment.objects.filter(order_id = order_id).exists():
        payment = Payment.objects.get(order_id=order_id)
        payment.is_paid = True
        payment.save()
        print(f"Платёж прошел успешно! Order ID: {order_id}")
    else:
        print('Ошибка')
    return redirect('http://localhost:3000')


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['client__email']
    
    def get_queryset(self):
        email = self.request.query_params.get('search', None)
        if email:
            return Payment.objects.filter(client__email=email)
        return Payment.objects.none()


