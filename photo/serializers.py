from rest_framework import serializers
from .models import Date, Photo

class PhotoSerializer(serializers.ModelSerializer):
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
