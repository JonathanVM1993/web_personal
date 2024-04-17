from django.urls import path
from .views import register_email

urlpatterns = [
    path('create_mail/', register_email, name='create_mail')    
]