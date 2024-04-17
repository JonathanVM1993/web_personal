import requests


def get_products(request):
    
    url = "http://127.0.0.1:9000/api/products/"
    payload = ""
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    productos = response.json()['data']

    return {'productos': productos}