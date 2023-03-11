from rest_framework import serializers

from products.serializers import ProductSerializer
from units.models import Supplier, BusinessUnit, Retailer, Wholesaler


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit.Contacts
        fields = '__all__'


class SuppliersListSerializer(serializers.ModelSerializer):
    contacts = ContactsSerializer()

    class Meta:
        model = Supplier
        many = True
        fields = '__all__'


class RetailerDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    contacts = ContactsSerializer()

    class Meta:
        model = Retailer
        fields = '__all__'
        read_only_fields = ['id', 'amount_due']


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = '__all__'
        read_only_fields = ['id', 'amount_due']


class RetailerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = '__all__'
        read_only_fields = ['id']


