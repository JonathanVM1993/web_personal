from django.shortcuts import render
from .models import Product
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Producto creado con éxito"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_all_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        products_serializer = ProductSerializer(products, many=True)
        return Response({"data": products_serializer.data})
    return Response({"data": products_serializer.errors, "message": "Error obteniendo los productos"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_product(request, pk=None):
    if request.method == 'GET': 
        product = Product.objects.filter(id = pk).first()
        product_serializer= ProductSerializer(product)        
        return Response({"data": product_serializer.data})
    return Response({"data": product_serializer.errors, "message": "Error obteniendo el producto"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk=None):
    if request.method == 'PUT':
        product = Product.objects.filter(id = pk).first()
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Producto modificado"}, status=status.HTTP_201_CREATED)
        return Response({"data": serializer.errors, "message": "Producto modificado sin éxito"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk=None):
    if request.method == 'DELETE':
        product = Product.objects.filter(id = pk).first()
        product.delete()
        return Response({"message": "Producto eliminado con éxito"}, status=status.HTTP_202_ACCEPTED)
    return Response({"message": "Error eliminando producto"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)