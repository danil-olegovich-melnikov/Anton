import shutil
from django.db import models
import os
from PIL import Image
from django.conf import settings

class Date(models.Model):
    date = models.DateField(verbose_name='Дата')

    class Meta:
        verbose_name = 'Дата'
        verbose_name_plural = 'Даты'

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')

def upload_to(instance, filename):
    # Временный путь для фото до получения ID
    return f'temp/{filename}'

class Photo(models.Model):
    date = models.ForeignKey('Date', on_delete=models.CASCADE, verbose_name='Дата')
    photo = models.ImageField('Фото', upload_to=upload_to)
    price = models.PositiveSmallIntegerField('Цена')
    watermark = models.ImageField('Защищенное фото', upload_to='', editable=False, blank=True)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        temp_name = self.photo.name

        super().save(*args, **kwargs)

        if is_new and 'temp/' in self.photo.path:
            ext = os.path.splitext(temp_name)[1]
            folder_date = self.date.date.isoformat()
            new_dir = f'{folder_date}/{self.id}'
            new_path = f'media/{new_dir}/origin{ext}'
            watermark_path = new_path.replace('origin', 'watermark')
            os.makedirs(os.path.dirname(new_path), exist_ok=True)

            shutil.move(self.photo.path, new_path)
            shutil.copy(new_path, watermark_path)
            self.photo.name = new_path[6:]  # remove 'media/'
            self.watermark.name = watermark_path[6:]

            # Открываем оригинальное фото
            image = Image.open(watermark_path).convert("RGBA")
            image = crop_center_resize(image, (300, 200))

            # Открываем и подготавливаем водяной знак
            wm_path = os.path.join(settings.STATICFILES_DIRS[0], 'watermark.png')
            if os.path.exists(wm_path):
                watermark = Image.open(wm_path).convert("RGBA").resize((300, 200))
                image.paste(watermark, (0, 0), watermark)

            # Сохраняем изображение
            image = image.convert("RGB")  # для совместимости с JPEG
            image.save(watermark_path, quality=90)

            super().save(update_fields=['photo', 'watermark'])



    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return f'Фото {self.id} на {self.date}'


def crop_center_resize(img, size):
    target_ratio = size[0] / size[1]
    width, height = img.size
    current_ratio = width / height

    if current_ratio > target_ratio:
        # Слишком широкое — обрезаем по ширине
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        img = img.crop((left, 0, left + new_width, height))
    else:
        # Слишком высокое — обрезаем по высоте
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        img = img.crop((0, top, width, top + new_height))

    return img.resize(size, Image.LANCZOS)


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
    date = models.DateField(auto_now=True)

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


