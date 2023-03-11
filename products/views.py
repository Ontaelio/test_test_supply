from django.shortcuts import render
from rest_framework import generics, permissions

from products.models import Product
from products.serializers import ProductSerializer


class ProductsListView(generics.ListAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CreateProductView(generics.CreateAPIView):
    serializer_class = ProductSerializer


