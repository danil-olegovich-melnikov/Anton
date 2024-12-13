from rest_framework import generics
from .models import Date
from .serializers import DateSerializer

class DateListAPIView(generics.ListAPIView):
    queryset = Date.objects.all()
    serializer_class = DateSerializer
