from django.urls import path
from .views import register_user, user_login, user_logout, user_update, recover_mail, change_password

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('update/<str:username>', user_update, name='update'),
    path('recover/', recover_mail, name='recover'),
    path('change_password/', change_password, name='change_password'),
]