from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from PIL import Image

class UserProfile(models.Model):
	user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
	tg_id = models.IntegerField(blank=True, null=True)
	tg_username = models.CharField(blank=True, null=True, verbose_name='Telegram Username', max_length=20)
	name = models.CharField(max_length=20 ,blank=True, verbose_name='Имя')
	balance = models.FloatField(default=0, verbose_name='Баланс')
	date_of_registration = models.DateField(auto_now_add=True)
	sales = models.ManyToManyField('Sale', related_name='sales', verbose_name='Покупки', blank=True)
	payments = models.ManyToManyField('Payment', related_name='payments', verbose_name='Платежи', blank=True)

	class Meta:
		verbose_name='Пользователь'
		verbose_name_plural='Пользователи'

	def __str__(self):
		return str(self.user.username)


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)



class Product(models.Model):
	name = models.CharField(verbose_name='Название товара', max_length=100)
	is_active = models.BooleanField(default=True, verbose_name='Включен')
	cost = models.IntegerField(verbose_name='Цена')
	description = models.TextField(verbose_name='Описание')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
	image = models.ImageField(verbose_name='Фото', upload_to='products/')
	is_counted = models.BooleanField(default=False, verbose_name='Несколько')
	successful_payment_answer = models.ManyToManyField('Good', verbose_name='После оплаты')
	date_added = models.DateField(auto_now_add=True)

	class Meta:
		verbose_name='Товар'
		verbose_name_plural='Товары'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 600 or img.width > 600:
			output_size = (600, 600)
			img = img.resize(output_size)
			img.save(self.image.path)

	def __str__(self):
		return str(self.name)


class Good(models.Model):
	is_unlimited = models.BooleanField(default=False, verbose_name='Бесконечный')
	data = models.TextField(verbose_name='Содержимое')

	class Meta:
		verbose_name='Содержимое'
		verbose_name_plural='Содержимое'

	def __str__(self):
		return str(self.data)


class Payment(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
	amount = models.FloatField(verbose_name='Количество')
	status = models.CharField(choices=[('waiting', 'Не оплачено'),
									   ('paid','Оплачено'),
									   ('canceled','Отменено')], verbose_name='Статус', max_length=20)
	date = models.DateField(auto_now=True, verbose_name='Дата')

	class Meta:
		verbose_name='Платеж'
		verbose_name_plural='Платежи'

	def __str__(self):
		return str(self.id)


class Sale(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
	count = models.FloatField(verbose_name='Количество')
	cost = models.FloatField(verbose_name='Стоимость')
	date = models.DateField(auto_now=True, verbose_name='Дата')
	status = models.CharField(choices=[('waiting', 'waiting'), ('paid', 'paid'), ('canceled', 'canceled')], max_length=10, verbose_name='Статус')

	class Meta:
		verbose_name='Покупка'
		verbose_name_plural='Покупки'

	def __str__(self):
		return str(self.id)