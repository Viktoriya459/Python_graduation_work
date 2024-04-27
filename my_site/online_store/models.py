from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва товару')
    slug = models.SlugField(max_length=255, unique=True, null=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Опис товару')
    size = models.ForeignKey('Size', on_delete=models.PROTECT, null=True , verbose_name='Розмір')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    photo = models.ImageField(upload_to='photos/', verbose_name='Фото')
    availability = models.BooleanField(default=True, verbose_name='Наявність')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категорія')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_page', kwargs={'prod_id': self.pk})

    class Meta:
        verbose_name = 'Дитячі товари'
        verbose_name_plural = 'Дитячі товари'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name = 'Категорія')
    slug = models.SlugField(max_length=255, unique=True, null=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['id']

class Size(models.Model):

    size_type = models.CharField(max_length=50)

    def __str__(self):
        return self.size_type


class Order(models.Model):

    name = models.CharField(max_length=100, verbose_name ="Ім'я")
    phone = models.CharField(max_length=20, verbose_name ='Номер телефону')
    email = models.EmailField()
    products = models.CharField(max_length=100, verbose_name ='Товари')
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name ='Загальна сума')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name ='Час створення')
    quantity = models.PositiveIntegerField(default=1, verbose_name ='Кількість')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['name']


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Повідомлення")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Зворотній зв\'язок'
        verbose_name_plural = 'Зворотній зв\'язок'
        ordering = ['created_at']



