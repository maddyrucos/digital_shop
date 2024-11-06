from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from PIL import Image
from django.dispatch import receiver

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	tg_id = models.IntegerField(blank=True, null=True)
	tg_username = models.CharField(blank=True, null=True, verbose_name='Telegram Username', max_length=20)
	name = models.CharField(max_length=20, blank=True, verbose_name='Имя')
	balance = models.IntegerField(default=0, verbose_name='Баланс')
	date_of_registration = models.DateField(auto_now_add=True)
	sales = models.ManyToManyField('Sale', related_name='sales', verbose_name='Покупки', blank=True)
	payments = models.ManyToManyField('Payment', related_name='payments', verbose_name='Платежи', blank=True)

	class Meta:
		verbose_name='Пользователь'
		verbose_name_plural='Пользователи'

	def __str__(self):
		return str(self.user.username)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	''' Connects the user model with userprofile models '''
	if created:
		UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Category(models.Model):
	name = models.CharField(max_length=255)
	parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

	def get_full_path(self):
		''' Displays full path (all parents) in admin '''
		if self.parent:
			return f'{str(self.parent.get_full_path())}->{str(self.name)}'
		else:
			return str(self.name)

	def __str__(self):
		return self.get_full_path()

	class Meta:
		verbose_name='Категория'
		verbose_name_plural='Категории'



class Product(models.Model):
	name = models.CharField(verbose_name='Название товара', max_length=100)
	is_active = models.BooleanField(default=True, verbose_name='Включен')
	price = models.IntegerField(verbose_name='Цена')
	description = models.TextField(verbose_name='Описание')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
	image = models.ImageField(verbose_name='Фото', upload_to='products/')
	is_multiple = models.BooleanField(default=False, verbose_name='Несколько')
	content = models.ManyToManyField('Content', verbose_name='После оплаты', related_name='answer')
	date_added = models.DateField(auto_now_add=True)

	class Meta:
		verbose_name='Товар'
		verbose_name_plural='Товары'

	def save(self, *args, **kwargs):
		''' Makes all the images in same size '''
		super().save(*args, **kwargs)
		img = Image.open(self.image.path)
		if img.height > 600 or img.width > 600:
			output_size = (600, 600)
			img = img.resize(output_size)
			img.save(self.image.path)

	def __str__(self):
		return str(self.name)


class Content(models.Model):
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
	count = models.IntegerField(verbose_name='Количество')
	total_cost = models.IntegerField(verbose_name='Стоимость')
	date = models.DateField(auto_now=True, verbose_name='Дата')
	content = models.TextField(default='Error')
	status = models.CharField(choices=[('waiting', 'waiting'), ('paid', 'paid'), ('canceled', 'canceled')], max_length=10, verbose_name='Статус')

	class Meta:
		verbose_name='Покупка'
		verbose_name_plural='Покупки'

	def __str__(self):
		return f'{self.id} - {self.product} - {self.customer} - {self.total_cost} - {self.status}'
