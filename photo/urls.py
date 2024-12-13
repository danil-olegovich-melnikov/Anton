from django.urls import path
from .views import DateListAPIView

urlpatterns = [
    path('dates/', DateListAPIView.as_view(), name='date-list'),
]
