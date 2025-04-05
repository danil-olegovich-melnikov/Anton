from django.urls import path
from .views import DateListAPIView, PaymentListView
from .views import payment_webhook, create_payment_view

urlpatterns = [
    path('dates/', DateListAPIView.as_view(), name='date-list'),
    path("payment_webhook/", payment_webhook, name="payment_webhook"),
    path("pay/", create_payment_view, name="create_payment"),
    path('orders/', PaymentListView.as_view(), name='orders-list'),
]
