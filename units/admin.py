import logging

from django.contrib import admin

from units.models import Factory, Retailer, Wholesaler, BusinessUnit


@admin.action(description='Сбросить задолженность')
def clear_due(modeladmin, request, queryset):
    queryset.update(amount_due=0)


@admin.register(Wholesaler, Retailer)
class CustomProvider(admin.ModelAdmin):
    list_display = ('name', 'supplier')
    list_display_links = ('name', 'supplier')
    list_filter = ('contacts__city',)
    actions = [clear_due, ]


@admin.register(Factory)
class CustomFactory(admin.ModelAdmin):
    list_filter = (('contacts', admin.RelatedOnlyFieldListFilter),)


admin.site.register(BusinessUnit.Contacts)
