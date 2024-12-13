from django.contrib import admin
from .models import Date, Photo
from django.utils.html import format_html

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    fields = ('display_photo', 'photo', 'price')
    readonly_fields = ('display_photo',)

    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 200px; max-height:200px;" />', obj.photo.url)
        return ""
    display_photo.short_description = 'Фото'



@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    list_display = ('date',)

    

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'display_photo', 'price')
    list_filter = ('date',)
    search_fields = ('date__date', 'price')

    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 200px; max-height:200px;" />', obj.photo.url)
        return "No Image"
    display_photo.short_description = 'Фото'
