from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)
    img = models.CharField(max_length=255, default="null")
    linkedin = models.CharField(max_length=255, default="null")
    #name = models.CharField(max_length=100)
    #password = models.CharField(max_length=100)

    def __str__(self):
        return self.username