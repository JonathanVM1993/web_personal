from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    description = models.TextField(max_length=500, default='null')
    img = models.CharField(max_length=255, default="null")
    created_at = models.DateTimeField(auto_now_add=True)
    uptated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=110)
    description = models.CharField(max_length=250)
    created_at = models.DateField()

    class Meta:
        # db_table : Nombre en la bdd

        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"