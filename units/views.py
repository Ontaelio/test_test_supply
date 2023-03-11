from django.shortcuts import render
from rest_framework import generics, permissions

from units.models import Supplier, Wholesaler, Retailer
from units.serializers import SuppliersListSerializer, RetailerSerializer, RetailerDetailSerializer, \
    RetailerCreateSerializer


class SupplierListView(generics.ListAPIView):
    model = Supplier
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SuppliersListSerializer

    def get_queryset(self):
        return Supplier.objects.prefetch_related('contacts')


class RetailersListView(generics.ListAPIView):
    serializer_class = RetailerDetailSerializer

    def get_queryset(self):
        queryset = Retailer.objects.prefetch_related('contacts')
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(contacts__country=country)
        return queryset


class RetailerCreateView(generics.CreateAPIView):
    serializer_class = RetailerCreateSerializer


class RetailerView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RetailerSerializer
    queryset = Retailer.objects.all()


class RetailerDetailedView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RetailerDetailSerializer
    queryset = Retailer.objects.all()
