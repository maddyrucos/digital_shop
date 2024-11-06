# Generated by Django 5.1.2 on 2024-11-06 19:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_unlimited', models.BooleanField(default=False, verbose_name='Бесконечный')),
                ('data', models.TextField(verbose_name='Содержимое')),
            ],
            options={
                'verbose_name': 'Содержимое',
                'verbose_name_plural': 'Содержимое',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shop.category')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='Количество')),
                ('status', models.CharField(choices=[('waiting', 'Не оплачено'), ('paid', 'Оплачено'), ('canceled', 'Отменено')], max_length=20, verbose_name='Статус')),
                ('date', models.DateField(auto_now=True, verbose_name='Дата')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название товара')),
                ('is_active', models.BooleanField(default=True, verbose_name='Включен')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to='products/', verbose_name='Фото')),
                ('is_multiple', models.BooleanField(default=False, verbose_name='Несколько')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Категория')),
                ('content', models.ManyToManyField(related_name='answer', to='shop.content', verbose_name='После оплаты')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Количество')),
                ('total_cost', models.IntegerField(verbose_name='Стоимость')),
                ('date', models.DateField(auto_now=True, verbose_name='Дата')),
                ('content', models.TextField(default='Error')),
                ('status', models.CharField(choices=[('waiting', 'waiting'), ('paid', 'paid'), ('canceled', 'canceled')], max_length=10, verbose_name='Статус')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.IntegerField(blank=True, null=True)),
                ('tg_username', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telegram Username')),
                ('name', models.CharField(blank=True, max_length=20, verbose_name='Имя')),
                ('balance', models.IntegerField(default=0, verbose_name='Баланс')),
                ('date_of_registration', models.DateField(auto_now_add=True)),
                ('payments', models.ManyToManyField(blank=True, related_name='payments', to='shop.payment', verbose_name='Платежи')),
                ('sales', models.ManyToManyField(blank=True, related_name='sales', to='shop.sale', verbose_name='Покупки')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
