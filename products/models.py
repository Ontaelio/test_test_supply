from django.db import models


class Product(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.CharField(max_length=1024)
    model = models.CharField(max_length=1024)
    date_presented = models.DateField()

    def __str__(self):
        return self.name



