from django.shortcuts import render, redirect
import requests
from django.contrib import messages
import json
from django.core.files.storage import FileSystemStorage
from django.template import RequestContext, Context, Template
from pathlib import Path
import os
import datetime
from django.contrib.auth.decorators import login_required

path_media_backend = Path(__file__).resolve().parent.parent
path_media_backend = "asd"
# Create your views here.

@login_required(login_url="welcome")
def products(request):

    return render(request, 'main/products.html')

@login_required(login_url="welcome")
def products_create(request):

    if request.method=='POST':        
        
        myfile = request.FILES['ufile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        

        url = "http://127.0.0.1:9000/api/product_create/"

        payload = json.dumps({
        "name": request.POST.get('name'),
        "price": request.POST.get('price'),
        "description": request.POST.get('description'),
        "img": uploaded_file_url
        })

        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + request.session.get('token')
        }

        response = requests.request("POST", url, headers=headers, data=payload)        

        if response.status_code==201:
            messages.success(request, f"Producto creado con éxito")
        elif response.status_code==401:
            messages.error(request, 'Necesitas crear un Usuario e Iniciar sesión para crear productos')
        else:
            messages.error(request, f'Ha ocurrido un error creando el producto.')

    return render(request, 'crud/products_create.html',{
        "title": 'Creacion de productos'
    })

@login_required(login_url="welcome")
def products_read_all(request):
    
    path_media_backend = str(Path(__file__).resolve().parent.parent.parent)+"/drf"

    if request.method=='GET':
        url = "http://127.0.0.1:9000/api/products/"

        payload = ""
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        productos = response.json()['data']
        

    return render(request, 'crud/products_read_all.html',{
        "productos": productos,
        "path_media_backend": path_media_backend,
        "title": 'Productos'
    })

@login_required(login_url="welcome")
def products_read(request):

    producto = ""
    search = False

    if request.method=='POST':
    
        url = f"http://127.0.0.1:9000/api/product/{request.POST.get('id')}"
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        producto = response.json()['data']

        search = True

    return render(request, 'crud/products_read.html',{        
        "selected": producto,
        "search": search,
        "title": 'Buscador de productos'
    })

@login_required(login_url="welcome")
def products_update(request):
    return render(request, 'crud/products_update.html',{
        "title": 'Modificacion de productos'
    })

@login_required(login_url="welcome")
def product_updating(request, id=None):

    url = f"http://127.0.0.1:9000/api/product/{id}"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    producto = response.json()['data']

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    seconds = datetime.datetime.now().second
    

    time = f"{year}{month}{day}{hour}{minute}{seconds}"

    if request.method == 'POST':

        if 'foto' in request.FILES:
            myfile = request.FILES['foto']
            fs = FileSystemStorage()
            filename = fs.save(f'{time}{myfile.name.replace(" ","")}', myfile)
            uploaded_file_url = fs.url(filename)
            name = producto['img']
            sub_string = name.split("/")
            fs.delete(f"{sub_string[2]}")     
        else:
            uploaded_file_url = producto['img']

        url = f"http://127.0.0.1:9000/api/product_update/{producto['id']}"

        payload = json.dumps({
        "name": request.POST.get('product_name'),
        "price": request.POST.get('product_price'),
        "description": request.POST.get('product_description'),
        "img": uploaded_file_url
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'Token ' + request.session.get('token')
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        if response.status_code == 201:
            return redirect('products_update')
        elif response.status_code == 401:
            messages.error(request, 'Necesitas crear un Usuario e Iniciar sesión para modificar productos')

    return render(request, 'crud/product_updating.html',{
        "name" : producto['name'],
        "price": producto['price'],
        "description": producto['description'],
        "img": uploaded_file_url,
        "status": response.status_code,
        "title": 'Modificando producto'
    })

@login_required(login_url="welcome")
def products_delete(request):

    if request.method == 'POST':

        url = f"http://127.0.0.1:9000/api/product_delete/{request.POST.get('id')}"

        payload = ""
        headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'Token ' + request.session.get('token')
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        if response.status_code == 201:
            return redirect('products_delete')
        elif response.status_code==401:
            messages.error(request, 'Necesitas crear un Usuario e Iniciar sesión para eliminar productos')

    return render(request, 'crud/products_delete.html',{
        "title": 'Eliminar producto'
    })
