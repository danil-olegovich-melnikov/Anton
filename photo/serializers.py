from rest_framework import serializers
from .models import Date, Photo

class PhotoSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    
    def get_photo(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.watermark.url)
        return obj.watermark.url
    
    class Meta:
        model = Photo
        fields = ['id', 'photo', 'price']

class PhotoSerializerOrigin(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'photo', 'price']

class DateSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True, source='photo_set')
    date = serializers.SerializerMethodField()

    def get_date(self, obj):
        print(1)
        return obj.date.strftime('%d.%m.%Y')
    
    class Meta:
        model = Date
        fields = ['id', 'date', 'photos']
from rest_framework import serializers
from .models import Date, Photo, Order, Payment


class DateSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True, source='photo_set')
    date = serializers.SerializerMethodField()

    def get_date(self, obj):
        return obj.date.strftime('%d.%m.%Y')
    
    class Meta:
        model = Date
        fields = ['id', 'date', 'photos']


class OrderSerializer(serializers.ModelSerializer):
    photo = PhotoSerializerOrigin()
    
    class Meta:
        model = Order
        fields = ['id', 'photo']

class PaymentSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True, source='order_set')
    
    class Meta:
        model = Payment
        fields = ['id', 'client', 'url', 'is_paid', 'orders']