from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products, name="products"),
    path('products_create/', views.products_create, name="products_create"),
    path('products_read_all/', views.products_read_all, name="products_read_all"),
    path('products_read/', views.products_read, name="products_read"),
    path('products_update/', views.products_update, name="products_update"),
    path('products_delete/', views.products_delete, name="products_delete"),
    path('product_updating/<int:id>', views.product_updating, name="product_updating")
]
