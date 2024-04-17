from django.shortcuts import render, HttpResponse, redirect
import requests
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib import messages
import numpy as np
from django.contrib.sessions.backends.db import SessionStore
from django.core.files.storage import FileSystemStorage, Storage
import json
import datetime
from django.contrib.auth import authenticate, login, logout

# Create your views here.

# Variables de Inicio


def welcome(request):    

    if request.user.is_authenticated:
        return redirect('inicio')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('inicio')
            else:
                messages.error(request, '¡No te has identificado correctamente!')

    return render(request, 'mainapp/welcome.html')

@login_required(login_url="welcome")
def index(request):
    
    title = "Portafolio Jonathan Varas"

    return render(request, 'mainapp/index.html',{
        'title': title
    })

@login_required(login_url="welcome")
def login_user(request):

    if request.method == 'POST':

        if request.session.get('logged_in') == False or request.session.get('logged_in') == None:
            if request.method == 'POST':

                url = "http://127.0.0.1:9000/api/login/"

                payload = {'username': request.POST.get('username'),
                'password': request.POST.get('password')}
                
                headers = {}

                response = requests.request("POST", url, headers=headers, data=payload)            

                if response.status_code == 200:     
                    request.session['token'] = response.json()["token"]                
                    request.session['logged_in'] = True
                    request.session['username'] = response.json()["username"]
                    request.session['first_name'] = response.json()["first_name"]                
                    request.session['email'] = response.json()["email"]
                    request.session['linkedin'] = response.json()["linkedin"]
                    request.session['img'] = response.json()["img"]

            else:
                request.session['logged_in'] = False

            if response.status_code == 201:            
                messages.success(request, f'Te has logueado correctamente')
            elif response.status_code == 401:
                messages.error(request, f"Error logueando usuario :{response.json()['error']}")
        

    return render(request, 'users/login.html',{        
        "token": request.session.get('token'),
        "logged_in": request.session.get('logged_in'),
        "title": 'Login de usuario'
    })

@login_required(login_url="welcome")
def register_user(request):

    registered = False

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    seconds = datetime.datetime.now().second

    time = f"{year}{month}{day}{hour}{minute}{seconds}"

    token = request.session.get('token')

    if token == None:
        token = "False"

        
    if request.method == 'POST':  

        url = "http://127.0.0.1:9000/api/register/"
            
        myfile = request.FILES['ufile']
        fs = FileSystemStorage()
        filename = fs.save(f'{time}{myfile.name.replace(" ","")}', myfile)
        uploaded_file_url = fs.url(filename)
            
        payload = json.dumps({
        "username": request.POST.get('user'),
        "first_name": request.POST.get('first_name'),
        "email": request.POST.get('email'),        
        "linkedin": request.POST.get('linkedin'), 
        "password": request.POST.get('password'),
        "img": uploaded_file_url
        })
            
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 201:
            messages.success(request, f'Has creado correctamente el Usuario')            
        elif response.status_code == 400:
            messages.error(request, f'Error creando usuario')
        


    return render(request, 'users/register.html',{
        'registered': registered,
        "title": 'Registro de usuario'
    })


@login_required(login_url="welcome")
def logout_user(request):

    token = request.session.get('token')

    if token == None:
        return redirect('inicio')
        
    url = "http://127.0.0.1:9000/api/logout/"

    payload = {}
    files={}
    headers = {
    'Authorization': 'Token '+ token
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    if response.status_code == 200:
        request.session['token'] = ''
        request.session['logged_in'] = False
        request.session['username'] = ""
        request.session['email'] = ""
        request.session['img'] = ""
        #request.session.flush()               
    elif response.status_code == 401:
        request.session['token'] = ''
        request.session['logged_in'] = False
        request.session['username'] = ""
        request.session['email'] = ""
        request.session['img'] = ""

    return render(request, 'users/logout.html',{
        'token': token
    })

@login_required(login_url="welcome")
def user_profile(request):

    return render(request, 'users/profile.html',{
        "title": 'Perfil de usuario'
    })


@login_required(login_url="welcome")
def user_update(request):
    
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    seconds = datetime.datetime.now().second  


    time = f"{year}{month}{day}{hour}{minute}{seconds}"

    if request.method == 'POST':

        fs = ""

        if 'foto' in request.FILES:
            myfile = request.FILES['foto']
            fs = FileSystemStorage()
            filename = fs.save(f'{time}{myfile.name.replace(" ","")}', myfile)
            uploaded_file_url = fs.url(filename)
            name = request.session.get('img')
            sub_string = name.split("/")
            
            fs.delete(f"{sub_string[2]}")            

        else:
            uploaded_file_url = request.session.get('img')
        

        # {myfile.name.split(".")[1]}
        url = f"http://127.0.0.1:9000/api/update/{request.session.get('username')}"

        payload = json.dumps({
        "first_name": request.POST.get('first_name'),
        "email": request.POST.get('email'),
        "linkedin": request.POST.get('linkedin'),
        "img": uploaded_file_url
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        if response.status_code == 201:            
            request.session['first_name'] = request.POST.get('first_name')
            request.session['email'] = request.POST.get('email')
            request.session['linkedin'] = request.POST.get('linkedin')
            request.session['img'] = uploaded_file_url
            messages.success(request, f"Éxito modificando el usuario")
        elif response.status_code == 500:
            messages.error(request, f"Error modificando el usuario")


    return render(request, 'users/update.html',{
        "title": 'Modificacion de usuario'
    })

@login_required(login_url="welcome")
def recover_password(request):

    if request.method == 'POST':       
        

        url = "http://127.0.0.1:9000/api/password_reset/"

        payload = json.dumps({
        "email": request.POST.get('email')
        })
        headers = {
        'Content-Type': 'application/json'
    }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            messages.success(request, "Se ha enviado un correo con el Link para cambiar la contraseña. Revise su Spam en caso de no encontrarlo.")
        elif response.status_code == 400:
            messages.error(request,f'Error enviando correo para recuperar contraseña' )

    return render(request, 'users/recover_password.html',{
        "title": 'Recuperacion de contraseña'
    })


@login_required(login_url="welcome")
def reset_password(request):

    if request.method == 'POST':

        if request.POST.get('pw1') != request.POST.get('pw2'):
            messages.error(request, 'Las contraseñas no coinciden')
        else:
            url = f"http://127.0.0.1:9000/api/password_reset/confirm/?token={request.POST.get('token')}"

            payload = json.dumps({
            "password": request.POST.get('pw1'),
            "token": request.POST.get('token')
            })
            headers = {
            'Content-Type': 'application/json'
        }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                messages.success(request, "Contraseña cambiada con éxito")

            elif response.status_code == 400:
                messages.error(request, f'Error reseteando contraseña')


    return render(request, 'users/reset_password.html',{
        "title": 'Reseteo de contraseña'
    })

@login_required(login_url="welcome")
def reset_password_2(request):

    if request.method == 'POST':

        url = "http://127.0.0.1:9000/api/change_password/"

        payload = json.dumps({
        "old_password": request.POST.get('old_pw'),
        "new_password": request.POST.get('new_pw')
        })
        headers = {
        'Authorization': f"Token {request.session.get('token')}",
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)        

        if response.status_code == 200:
            messages.success(request, "Contraseña cambiada con éxito")

        elif response.status_code == 400:
            messages.error(request, f'Error reseteando contraseña')


    return render(request, 'users/reset_password_2.html',{
        "title": 'Reseteo de contraseña'
    })

def exit(request):
    request.session.flush()
    request.session['token'] = ''
    request.session['logged_in'] = False
    request.session['username'] = ""
    request.session['email'] = ""
    request.session['img'] = ""

    return redirect('welcome')