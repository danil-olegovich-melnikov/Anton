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
