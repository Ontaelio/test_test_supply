from django.db import models
from django_countries.fields import CountryField

from products.models import Product


class BusinessUnit(models.Model):
    class Meta:
        abstract = True

    class Contacts(models.Model):
        class Meta:
            verbose_name = 'Контакт'
            verbose_name_plural = 'Контакты'

        email = models.EmailField(verbose_name='email')
        country = CountryField(verbose_name='Страна')
        city = models.CharField(max_length=1024, verbose_name='Город')
        street = models.CharField(max_length=1024, verbose_name='Улица')
        street_number = models.CharField(max_length=50, verbose_name='Номер дома')

        def __str__(self):
            return self.city

    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    contacts = models.ForeignKey(Contacts, on_delete=models.PROTECT,
                                 related_name="%(class)s_unit", verbose_name='Контакты')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.name


class Supplier(BusinessUnit):
    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


# class Procurer(models.Model):
#     class Meta:
#         verbose_name = 'Покупатель'
#         verbose_name_plural = 'Покупатели'
#
#     supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT,
#                                  related_name='wholesalers', verbose_name='Поставщик')
#     products = models.ManyToManyField(Product, related_name='wholesalers')
#     amount_due = models.BigIntegerField()


class Factory(Supplier):
    class Meta:
        verbose_name = 'Завод'
        verbose_name_plural = 'Заводы'


class Wholesaler(Supplier):
    class Meta:
        verbose_name = 'Оптовик'
        verbose_name_plural = 'Оптовики'

    supplier = models.ForeignKey(Factory, on_delete=models.PROTECT,
                                 related_name='wholesalers', verbose_name='Поставщик')
    products = models.ManyToManyField(Product, related_name='wholesalers')
    amount_due = models.BigIntegerField()


class Retailer(BusinessUnit):
    class Meta:
        verbose_name = 'Розница'
        verbose_name_plural = 'Розница'

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT,
                                 related_name='retail_outlets', verbose_name='Поставщик')
    products = models.ManyToManyField(Product, related_name='retail_outlets')
    amount_due = models.BigIntegerField()
