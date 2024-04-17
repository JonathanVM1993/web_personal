from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser
from mail.models import RecoverMail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.contrib.auth import update_session_auth_hash
from .serializers import ChangePasswordSerializer



@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Creado con éxito"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None

        """
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)

            except ObjectDoesNotExist:
                pass
        """
        
        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token,_ = Token.objects.get_or_create(user=user)
            
            return Response({'token': token.key, 'username': username,'first_name': user.first_name,'email':user.email, 'linkedin': user.linkedin,'img': user.img}, status=status.HTTP_200_OK)        
        
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   


@api_view(['PUT'])
def user_update(request, username=None):    
    if request.method == 'PUT':
        user = CustomUser.objects.filter(username = username).first()
        user.first_name = request.data['first_name']
        user.email = request.data['email']
        user.linkedin = request.data['linkedin']
        user.img = request.data['img']
        user.save()
        return Response({"message": "Usuario Modificado con éxito"}, status=status.HTTP_201_CREATED)
    return Response({"message": f"Usuario modificado sin éxito {request.data['first_name']}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def recover_mail(request):
    if request.method == 'POST':
        

        return Response({"message": "Correo enviado con éxito"}, status=status.HTTP_200_OK)
    return Response({"message": "Error enviando correo de recuperación"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)