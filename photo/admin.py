from django.contrib import admin
from .models import Date, Photo, Client, Payment, Order
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

class OrderInline(admin.TabularInline):
    model = Order
    extra = 1


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


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ('email',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    search_fields = ("client",)
    list_display = ('id', 'client', 'display_price', 'is_paid', 'order_id')
    inlines = (OrderInline,)
    fields = ('display_price', 'client', 'url', 'is_paid', 'order_id')
    readonly_fields = ('display_price', 'url', 'is_paid')

    def display_price(self, obj):
        total_price = sum(order.photo.price for order in obj.order_set.all())
        return total_price

    display_price.short_description = 'Сумма заказа'
