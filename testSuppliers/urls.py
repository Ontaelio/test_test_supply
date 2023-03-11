from django.contrib import admin
from django.urls import path, re_path

from units import views as unit_views
from products import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('products/create', product_views.CreateProductView.as_view(), name='create-product'),
    path('products/<pk>', product_views.ProductView.as_view(), name='product-view'),
    re_path(r'products/$', product_views.ProductsListView.as_view(), name='products-list'),

    re_path(r'suppliers/$', unit_views.SupplierListView.as_view(), name='suppliers-list'),

    path('retailers/create', unit_views.RetailerCreateView.as_view(), name='retailer-create'),
    path('retailers/<pk>/details', unit_views.RetailerDetailedView.as_view(), name='retailer-details'),
    path('retailers/<pk>', unit_views.RetailerView.as_view(), name='retailer-view'),
    re_path(r"retailers/$", unit_views.RetailersListView.as_view(), name='retailers-list'),
]
