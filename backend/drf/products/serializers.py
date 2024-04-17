from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'price', 'description','img']

    def create(self, data):
        product = Product(
            name = data['name'],
            price = data['price'],
            description = data['description'],
            img = data['img']
        )
        product.save()
        return product