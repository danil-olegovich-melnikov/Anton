from django.db import models

class Date(models.Model):
    date = models.DateField(verbose_name='Дата')

    class Meta:
        verbose_name = 'Дата'
        verbose_name_plural = 'Даты'

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')


class Photo(models.Model):
    date = models.ForeignKey(Date, on_delete=models.CASCADE, verbose_name='Дата')
    photo = models.ImageField('Фото', upload_to='photos/')
    price = models.PositiveSmallIntegerField('Цена')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return f'Фото {self.id} на {self.date}'


class Client(models.Model):
    email = models.EmailField("Почта", unique=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.email

class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    url = models.CharField("Ссылка на оплату", max_length=256)
    order_id = models.UUIDField(verbose_name='ID заказа')
    is_paid = models.BooleanField("Оплачено", default=False)

    def __str__(self):
        return f"Заказ №{self.id}"
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class Order(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, verbose_name="Оплата")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name="Фотография")
    
    def __str__(self):
        return f"Заказ {self.id}"


