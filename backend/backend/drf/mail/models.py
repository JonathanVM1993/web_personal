from django.db import models
from django import forms

# Create your models here.

class RecoverMail(models.Model):

    email = models.CharField(max_length=200)
    password = models.CharField(max_length= 200, default = "null")

    def __str__(self):
        return self.email
