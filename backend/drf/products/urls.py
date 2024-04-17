from django.urls import path
from .views import create_product, update_product, get_all_products, get_product, delete_product

urlpatterns = [
    path('product_create/', create_product, name='create_product'),
    path('products/', get_all_products, name='get_products'),
    path('product/<int:pk>', get_product, name="get_product"),    
    path('product_update/<int:pk>', update_product, name='update_product'),
    path('product_delete/<int:pk>', delete_product, name='delete_product')
]