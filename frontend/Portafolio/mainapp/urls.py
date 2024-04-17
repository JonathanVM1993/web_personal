from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('welcome/', views.welcome, name="welcome"),
    path('inicio/', views.index, name="inicio"),
    path('login/', views.login_user, name="login"),
    path('registro/', views.register_user, name="registro"), 
    path('logout/', views.logout_user, name="logout"),
    path('profile/', views.user_profile, name="profile"),
    path('update/', views.user_update, name="update"),    
    path('recover_password/', views.recover_password, name="recover_password"),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_2/', views.reset_password_2, name='reset_password_2'),
    path('exit/', views.exit, name="exit")
]