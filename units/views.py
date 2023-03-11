from django.db.models import ProtectedError
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, status
from rest_framework.response import Response

from units.models import Supplier, Wholesaler, Retailer
from units.serializers import SuppliersListSerializer, RetailerSerializer, RetailerDetailSerializer, \
    RetailerCreateSerializer, FactoryDetailSerializer, WholesalerSerializer, WholesalerDetailSerializer, \
    WholesalerCreateSerializer


@extend_schema_view(
    get=extend_schema(description='Get a verbose list of all suppliers',
                      summary='Suppliers list')
)
class SupplierListView(generics.ListAPIView):
    model = Supplier
    serializer_class = SuppliersListSerializer

    def get_queryset(self):
        return Supplier.objects.prefetch_related('contacts')


@extend_schema_view(
    get=extend_schema(description='Get a verbose list of all factories. Can be sorted with ?country=XX (ISO 3166).',
                      summary='Factories list')
)
class FactoriesListView(generics.ListAPIView):
    serializer_class = FactoryDetailSerializer

    def get_queryset(self):
        queryset = Supplier.objects.prefetch_related('contacts').filter(factoryunit__isnull=False)
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(contacts__country=country)
        return queryset


@extend_schema_view(
    get=extend_schema(description='Get a verbose list of all wholesalers. Can be sorted with ?country=XX (ISO 3166).',
                      summary='Wholesalers list')
)
class WholesalersListView(generics.ListAPIView):
    serializer_class = WholesalerDetailSerializer

    def get_queryset(self):
        queryset = Wholesaler.objects.prefetch_related('contacts')
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(contacts__country=country)
        return queryset


@extend_schema_view(
    post=extend_schema(description='Create a wholesaler object. Must be connected to a supplier (factory).',
                       summary='Create wholesaler')
)
class WholesalerCreateView(generics.CreateAPIView):
    serializer_class = WholesalerCreateSerializer


@extend_schema_view(
    get=extend_schema(description='Short info on a wholesaler.',
                      summary='Wholesaler short'),
    put=extend_schema(description='Change all fields of a wholesaler except amount_due.',
                      summary='Wholesaler put'),
    patch=extend_schema(description='Change field(s) of a wholesaler except amount_due.',
                        summary='Wholesaler patch'),
    delete=extend_schema(description='Remove a wholesaler (note that connected retailers must be removed first).' 
                                     'The unit must not owe any money, else error 409.',
                         summary='Wholesaler delete'),
)
class WholesalerView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WholesalerSerializer
    queryset = Wholesaler.objects.all()

    def destroy(self, request, *args, **kwargs):
        """
            We don't want to delete a business unit that owes money.
        """
        instance = self.get_object()

        if instance.amount_due:
            return Response({'Error:': 'Amount due not zero'}, status=status.HTTP_409_CONFLICT)
        try:
            instance.delete()
        except ProtectedError:
            return Response({'Error:': 'Has dependencies'}, status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(description='Get a detailed wholesaler info',
                      summary='Detailed info')
)
class WholesalerDetailedView(generics.RetrieveAPIView):
    serializer_class = WholesalerDetailSerializer
    queryset = Wholesaler.objects.all()


@extend_schema_view(
    get=extend_schema(description='Get a verbose list of all retailers. Can be sorted with ?country=XX (ISO 3166).',
                      summary='Retailers list')
)
class RetailersListView(generics.ListAPIView):
    serializer_class = RetailerDetailSerializer

    def get_queryset(self):
        queryset = Retailer.objects.prefetch_related('contacts')
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(contacts__country=country)
        return queryset


@extend_schema_view(
    post=extend_schema(description='Create a retailer object. Must be connected to a supplier (factory or wholesaler).',
                       summary='Create retail outlet')
)
class RetailerCreateView(generics.CreateAPIView):
    serializer_class = RetailerCreateSerializer


@extend_schema_view(
    get=extend_schema(description='Short info on a retailer.',
                      summary='Retailer short'),
    put=extend_schema(description='Change all fields of a retailer except amount_due.',
                      summary='Retailer put'),
    patch=extend_schema(description='Change field(s) of a retailer except amount_due.',
                        summary='Retailer patch'),
    delete=extend_schema(description='Remove a retailer if it does not owe money (else error 409).',
                         summary='Retailer delete'),
)
class RetailerView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RetailerSerializer
    queryset = Retailer.objects.all()

    def destroy(self, request, *args, **kwargs):
        """
            We don't want to delete a business unit that owes money.
        """
        instance = self.get_object()

        if instance.amount_due:
            return Response({'Error:': 'Amount due not zero'}, status=status.HTTP_409_CONFLICT)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(description='Get a detailed wholesaler info',
                      summary='Detailed info')
)
class RetailerDetailedView(generics.RetrieveAPIView):
    serializer_class = RetailerDetailSerializer
    queryset = Retailer.objects.all()
