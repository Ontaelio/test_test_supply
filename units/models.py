from django.db import models
from django_countries.fields import CountryField

from products.models import Product


class BusinessUnit(models.Model):

    class Contacts(models.Model):
        email = models.EmailField(verbose_name='email')
        country = CountryField(verbose_name='Страна')
        city = models.CharField(max_length=1024, verbose_name='Город')
        street = models.CharField(max_length=1024, verbose_name='Улица')
        str_num = models.CharField(max_length=50, verbose_name='Номер дома')
        verbose_name = 'Контакты'

    name = models.CharField(max_length=255, verbose_name='Название')
    contacts = Contacts
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.name


class Factory(BusinessUnit):
    class Meta:
        verbose_name = 'Завод'
        verbose_name_plural = 'Заводы'


class Wholesaler(BusinessUnit):
    class Meta:
        verbose_name = 'Оптовик'
        verbose_name_plural = 'Оптовики'

    supplier = models.ForeignKey(Factory, on_delete=models.PROTECT, verbose_name='Поставщик')
    products = models.ManyToManyField(Product)
    amount_due = models.BigIntegerField()


class Retailer(BusinessUnit):
    class Meta:
        verbose_name = 'Розница'
        verbose_name_plural = 'Розница'

    supplier = models.ForeignKey(BusinessUnit, on_delete=models.PROTECT, verbose_name='Поставщик')
    products = models.ManyToManyField(Product)
    amount_due = models.BigIntegerField()
